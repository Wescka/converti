from __future__ import annotations

import hashlib
import mimetypes
import os
import shutil
import subprocess
import threading
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

from werkzeug.utils import secure_filename

from config import (
    COMMAND_TIMEOUT_SECONDS,
    MAX_CONCURRENT_JOBS,
    RATE_LIMIT_PER_MINUTE,
    TEMP_DIR,
)

try:
    import magic
except Exception:
    magic = None

EXECUTABLE_MIMES = {
    "application/x-dosexec",
    "application/x-msdownload",
    "application/x-executable",
    "application/x-mach-binary",
    "application/vnd.microsoft.portable-executable",
}
EXECUTABLE_EXTS = {"exe", "dll", "com", "scr", "msi", "bat", "cmd", "ps1", "jar"}

JOB_SEMAPHORE = threading.BoundedSemaphore(MAX_CONCURRENT_JOBS)
_RATE_BUCKETS: dict[str, deque[float]] = defaultdict(deque)
_RATE_LOCK = threading.Lock()


def normalize_ext(value: str) -> str:
    ext = (value or "").strip().lower().lstrip(".")
    return {
        "jpeg": "jpg",
        "tif": "tiff",
        "htm": "html",
        "markdown": "md",
        "mpeg4": "mp4",
    }.get(ext, ext)


def safe_ext(filename: str) -> str:
    return normalize_ext(Path(filename).suffix.lstrip("."))


def safe_original_name(filename: str) -> str:
    return secure_filename(filename or "") or "archivo"


def random_file(ext: str, prefix: str = "cv") -> Path:
    ext = normalize_ext(ext) or "bin"
    return TEMP_DIR / f"{prefix}_{uuid.uuid4().hex}.{ext}"


def sha256_short(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def detect_mime(path: Path, original_name: str = "") -> str:
    if magic is not None:
        try:
            detector = magic.Magic(mime=True)
            value = detector.from_file(str(path))
            if value:
                return value.split(";", 1)[0].strip().lower()
        except Exception:
            pass
    guessed, _ = mimetypes.guess_type(original_name or path.name)
    return (guessed or "application/octet-stream").lower()


def validate_not_executable(path: Path, original_name: str, mime: str) -> None:
    ext = safe_ext(original_name)
    if ext in EXECUTABLE_EXTS or mime in EXECUTABLE_MIMES:
        raise ValueError("Por seguridad, Converti no procesa archivos ejecutables o scripts.")
    try:
        sig = path.read_bytes()[:4]
        if sig[:2] == b"MZ":
            raise ValueError("El contenido parece un ejecutable de Windows y fue rechazado.")
    except OSError:
        pass


def find_tool(*names: str, extra_paths: list[str] | None = None) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    for raw in extra_paths or []:
        p = Path(os.path.expandvars(raw))
        if p.exists():
            return str(p)
    return None


@dataclass(frozen=True)
class Toolchain:
    ffmpeg: str | None
    ffprobe: str | None
    soffice: str | None
    pandoc: str | None
    magick: str | None
    tesseract: str | None

    @property
    def as_dict(self) -> dict[str, bool]:
        return {
            "ffmpeg": bool(self.ffmpeg),
            "ffprobe": bool(self.ffprobe),
            "libreoffice": bool(self.soffice),
            "pandoc": bool(self.pandoc),
            "imagemagick": bool(self.magick),
            "tesseract_ocr": bool(self.tesseract),
            "python_magic": bool(magic),
        }


def get_toolchain() -> Toolchain:
    return Toolchain(
        ffmpeg=find_tool("ffmpeg", extra_paths=[r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe"]),
        ffprobe=find_tool("ffprobe", extra_paths=[r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffprobe.exe"]),
        soffice=find_tool(
            "soffice",
            "libreoffice",
            extra_paths=[
                r"%PROGRAMFILES%\LibreOffice\program\soffice.exe",
                r"%PROGRAMFILES(X86)%\LibreOffice\program\soffice.exe",
                r"%LOCALAPPDATA%\Programs\LibreOffice\program\soffice.exe",
            ],
        ),
        pandoc=find_tool("pandoc", extra_paths=[r"%LOCALAPPDATA%\Pandoc\pandoc.exe"]),
        magick=find_tool(
            "magick",
            extra_paths=[
                r"%LOCALAPPDATA%\Programs\ImageMagick\magick.exe",
                r"%PROGRAMFILES%\ImageMagick-7.1.2-Q16-HDRI\magick.exe",
            ],
        ),
        tesseract=find_tool(
            "tesseract",
            extra_paths=[
                r"%PROGRAMFILES%\Tesseract-OCR\tesseract.exe",
                r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe",
            ],
        ),
    )


def run_command(args: list[str], timeout: int | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    kwargs = dict(
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout or COMMAND_TIMEOUT_SECONDS,
        check=False,
        cwd=str(cwd) if cwd else None,
    )
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    result = subprocess.run(args, **kwargs)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "Error desconocido del motor de conversión").strip()
        raise RuntimeError(detail[-3000:])
    return result


def friendly_engine_error(exc: Exception) -> str:
    msg = str(exc)
    low = msg.lower()
    if "not found" in low or "no se reconoce" in low:
        return "Falta instalar o configurar el motor necesario para esta conversión."
    if "permission" in low or "access is denied" in low:
        return "El motor no tiene permisos suficientes para procesar este archivo."
    if "timeout" in low or "timed out" in low:
        return "La conversión excedió el tiempo máximo permitido."
    if "policy" in low and "imagemagick" in low:
        return "ImageMagick bloqueó esta operación por su política de seguridad."
    return "No se pudo completar la conversión con el motor disponible. Detalle técnico: " + msg[-500:]


def rate_limit_ok(key: str) -> bool:
    now = time.time()
    with _RATE_LOCK:
        q = _RATE_BUCKETS[key]
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= RATE_LIMIT_PER_MINUTE:
            return False
        q.append(now)
        return True

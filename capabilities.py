from __future__ import annotations

import re
from functools import lru_cache

from security_utils import Toolchain, normalize_ext, run_command

# Versión ONLINE / Render Free.
# Regla: solo anunciamos conversiones con una ruta clara en los motores actuales.
# Si una combinación es dudosa, costosa o el código no la implementa de forma
# explícita, NO se ofrece al usuario.

IMAGE_OUTPUTS = ["png", "jpg", "webp", "bmp", "gif", "tiff", "pdf"]
IMAGE_DOCUMENT_OUTPUTS = ["docx", "pptx", "html"]
AUDIO_OUTPUTS = ["mp3", "wav", "flac", "ogg", "opus", "m4a", "aac"]
VIDEO_OUTPUTS = ["mp4", "mkv", "avi", "webm", "mov"]

IMAGE_EXTS = {
    "jpg", "jpeg", "png", "webp", "bmp", "gif", "tif", "tiff", "ico",
    "avif", "heic", "heif", "svg", "psd", "jp2", "j2k", "jxl",
    "dng", "cr2", "cr3", "nef", "arw", "raf", "rw2", "orf"
}
AUDIO_EXTS = {
    "mp3", "wav", "flac", "ogg", "oga", "opus", "aac", "m4a", "wma",
    "aiff", "aif", "amr", "ape", "alac", "ac3"
}
VIDEO_EXTS = {
    "mp4", "mkv", "avi", "webm", "mov", "mpeg", "mpg", "m4v", "flv",
    "wmv", "3gp", "ts", "mts", "m2ts", "vob", "ogv"
}
TEXT_EXTS = {"txt", "md", "markdown", "rst", "tex", "latex", "html", "htm"}
DATA_EXTS = {"csv", "xlsx", "xls", "ods", "json", "xml"}
DOCUMENT_EXTS = {"pdf", "doc", "docx", "odt", "rtf", "ppt", "pptx", "odp", "epub"}


def detect_category(mime: str, ext: str) -> str:
    ext = normalize_ext(ext)
    mime = (mime or "").lower()

    if ext in DATA_EXTS:
        return "data"
    if mime.startswith("image/") or ext in IMAGE_EXTS:
        return "image"
    if mime.startswith("audio/") or ext in AUDIO_EXTS:
        return "audio"
    if mime.startswith("video/") or ext in VIDEO_EXTS:
        return "video"
    if mime.startswith("text/") or ext in TEXT_EXTS:
        return "text"

    office_words = (
        "pdf", "word", "officedocument", "opendocument", "rtf",
        "presentation", "powerpoint", "epub"
    )
    if ext in DOCUMENT_EXTS or any(word in mime for word in office_words):
        return "document"
    return "unknown"


@lru_cache(maxsize=8)
def ffmpeg_muxers(ffmpeg_path: str) -> set[str]:
    try:
        out = run_command([ffmpeg_path, "-hide_banner", "-muxers"], timeout=20).stdout
        muxers: set[str] = set()
        for line in out.splitlines():
            match = re.match(r"\s*[D\.]E\s+([^\s]+)", line)
            if match:
                muxers.update(normalize_ext(x) for x in match.group(1).split(","))
        return muxers
    except Exception:
        return set()


@lru_cache(maxsize=4)
def pandoc_outputs(pandoc_path: str) -> set[str]:
    try:
        out = run_command([pandoc_path, "--list-output-formats"], timeout=20).stdout
        return {normalize_ext(x.strip()) for x in out.splitlines() if x.strip()}
    except Exception:
        return set()


@lru_cache(maxsize=4)
def imagemagick_writable(magick_path: str) -> set[str]:
    try:
        out = run_command([magick_path, "-list", "format"], timeout=30).stdout
        result: set[str] = set()
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[0].isupper() and "w" in parts[2].lower():
                result.add(normalize_ext(parts[0].lower()))
        return result
    except Exception:
        return set()


def _pandoc_target_available(tools: Toolchain, target: str) -> bool:
    if not tools.pandoc:
        return False
    supported = pandoc_outputs(tools.pandoc)
    if not supported:
        return True
    aliases = {
        "md": "gfm",
        "txt": "plain",
        "html": "html",
        "tex": "latex",
    }
    return normalize_ext(aliases.get(target, target)) in supported


def _add_unique(result: list[str], values: list[str], source_ext: str) -> None:
    for value in values:
        value = normalize_ext(value)
        if value and value != source_ext and value not in result:
            result.append(value)


def targets_for(category: str, source_ext: str, tools: Toolchain) -> list[str]:
    source_ext = normalize_ext(source_ext)
    result: list[str] = []

    # VIDEO: activo en el servidor Termux/Redmi mediante FFmpeg.
    if category == "video":
        if not tools.ffmpeg:
            return []
        muxers = ffmpeg_muxers(tools.ffmpeg)
        allowed = []
        mux_alias = {"mkv": "matroska", "mov": "mov", "mp4": "mp4", "avi": "avi", "webm": "webm"}
        for target in VIDEO_OUTPUTS:
            check = mux_alias.get(target, target)
            if not muxers or target in muxers or check in muxers:
                allowed.append(target)
        # También permite extraer audio de un video.
        allowed += [x for x in AUDIO_OUTPUTS if x not in allowed]
        _add_unique(result, allowed, source_ext)
        return result

    # IMÁGENES: conversión de imagen y documentos contenedores.
    # PDF/DOCX/PPTX/HTML no dependen de que ImageMagick pueda *escribir* ese
    # formato: Converti rasteriza/normaliza primero la imagen y luego construye
    # el documento con sus motores Python. TXT/ODT/RTF se ofrecen solo cuando
    # existe el motor requerido (OCR / LibreOffice).
    if category == "image":
        if tools.magick:
            writable = imagemagick_writable(tools.magick)
            allowed = []
            for target in ["png", "jpg", "webp", "bmp", "gif", "tiff"]:
                check = "jpeg" if target == "jpg" else target
                if not writable or target in writable or check in writable:
                    allowed.append(target)
            _add_unique(result, allowed, source_ext)
        else:
            # Pillow cubre los formatos raster más comunes. Los formatos que
            # requieran un decodificador externo fallarán con un mensaje claro.
            _add_unique(result, ["png", "jpg", "webp", "bmp", "gif", "tiff"], source_ext)

        _add_unique(result, ["pdf"] + IMAGE_DOCUMENT_OUTPUTS, source_ext)
        if tools.tesseract:
            _add_unique(result, ["txt"], source_ext)
        if tools.soffice:
            _add_unique(result, ["odt", "rtf"], source_ext)
        return result

    # AUDIO: FFmpeg solamente, con formatos comunes.
    if category == "audio":
        if not tools.ffmpeg:
            return []
        muxers = ffmpeg_muxers(tools.ffmpeg)
        allowed = []
        for target in AUDIO_OUTPUTS:
            if not muxers:
                allowed.append(target)
            elif target == "m4a" and ("ipod" in muxers or "mp4" in muxers):
                allowed.append(target)
            elif target in muxers:
                allowed.append(target)
        _add_unique(result, allowed, source_ext)
        return result

    # DATOS ESTRUCTURADOS: estas rutas pasan por pandas / convert_structured.
    # XLS y ODS se ocultan por ahora porque la instalación actual no garantiza
    # los lectores adicionales necesarios en Render (xlrd / odfpy).
    if category == "data":
        matrix = {
            "csv":  ["xlsx", "json", "xml", "txt"],
            "xlsx": ["csv", "json", "xml", "txt"],
            "json": ["csv", "xlsx", "xml", "txt"],
            "xml":  ["csv", "xlsx", "json", "txt"],
            "xls":  [],
            "ods":  [],
        }
        _add_unique(result, matrix.get(source_ext, []), source_ext)
        return result

    # TEXTO: Pandoc es la ruta principal. Nada de CSV/XLSX/PPTX.
    if category == "text":
        candidates = {
            "txt":  ["html", "md", "docx", "odt", "rtf", "epub"],
            "md":   ["html", "txt", "docx", "odt", "rtf", "epub"],
            "html": ["md", "txt", "docx", "odt", "rtf", "epub"],
            "rst":  ["html", "md", "txt", "docx", "odt", "rtf"],
            "tex":  ["html", "md", "txt", "docx", "odt", "rtf"],
        }
        src = {"markdown": "md", "htm": "html", "latex": "tex"}.get(source_ext, source_ext)
        values = [x for x in candidates.get(src, []) if _pandoc_target_available(tools, x)]
        _add_unique(result, values, source_ext)
        return result

    if category != "document":
        return []

    # PDF usa nuestros conversores propios, no LibreOffice.
    if source_ext == "pdf":
        _add_unique(result, ["docx", "txt", "md", "html", "png", "jpg"], source_ext)
        return result

    # WORD / DOCX: motor nativo de Converti en Termux.
    # No depende de LibreOffice ni Pandoc para las salidas principales.
    if source_ext == "docx":
        _add_unique(result, ["pdf", "txt", "html", "md"], source_ext)
        # Si existen motores adicionales, ampliamos sin anunciar rutas falsas.
        if tools.soffice:
            _add_unique(result, ["odt", "rtf"], source_ext)
        if tools.pandoc:
            _add_unique(result, [x for x in ["epub"] if _pandoc_target_available(tools, x)], source_ext)
        return result

    if source_ext == "doc":
        # DOC antiguo: mantenemos solo conversiones directas fiables de LibreOffice.
        if tools.soffice:
            _add_unique(result, ["pdf", "docx", "odt", "rtf"], source_ext)
        return result

    if source_ext == "odt":
        if tools.soffice:
            _add_unique(result, ["pdf", "docx", "rtf"], source_ext)
        if tools.pandoc:
            _add_unique(result, [x for x in ["txt", "html", "md", "epub"] if _pandoc_target_available(tools, x)], source_ext)
        return result

    if source_ext == "rtf":
        if tools.soffice:
            _add_unique(result, ["pdf", "docx", "odt"], source_ext)
        if tools.pandoc:
            _add_unique(result, [x for x in ["txt", "html", "md"] if _pandoc_target_available(tools, x)], source_ext)
        return result

    # PRESENTACIONES: no CSV, no XLSX, no Word.
    if source_ext == "pptx":
        if tools.soffice:
            _add_unique(result, ["pdf", "odp"], source_ext)
        return result

    if source_ext == "ppt":
        if tools.soffice:
            _add_unique(result, ["pdf", "pptx", "odp"], source_ext)
        return result

    if source_ext == "odp":
        if tools.soffice:
            _add_unique(result, ["pdf", "pptx"], source_ext)
        return result

    # EPUB: Pandoc solamente.
    if source_ext == "epub":
        if tools.pandoc:
            _add_unique(
                result,
                [x for x in ["docx", "odt", "rtf", "txt", "html", "md"] if _pandoc_target_available(tools, x)],
                source_ext,
            )
        return result

    return []

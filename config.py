from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "archivos"
TEMP_DIR.mkdir(exist_ok=True)

MAX_MB = int(os.getenv("CONVERTI_MAX_MB", "200"))
TEMP_TTL_SECONDS = int(os.getenv("CONVERTI_TTL_SECONDS", str(30 * 60)))
CLEAN_INTERVAL_SECONDS = int(os.getenv("CONVERTI_CLEAN_INTERVAL", "300"))
COMMAND_TIMEOUT_SECONDS = int(os.getenv("CONVERTI_COMMAND_TIMEOUT", "900"))
MAX_CONCURRENT_JOBS = int(os.getenv("CONVERTI_MAX_CONCURRENT", "2"))
RATE_LIMIT_PER_MINUTE = int(os.getenv("CONVERTI_RATE_PER_MIN", "30"))
MAX_PDF_PAGES = int(os.getenv("CONVERTI_MAX_PDF_PAGES", "500"))
MAX_IMAGE_PIXELS = int(os.getenv("CONVERTI_MAX_IMAGE_PIXELS", "100000000"))

ALLOWED_PREVIEW_TEXT_BYTES = 20000

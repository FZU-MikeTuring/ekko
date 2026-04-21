from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_ROOT = BASE_DIR / "uploads"
AVATAR_UPLOAD_ROOT = UPLOAD_ROOT / "avatars"
USER_AVATAR_DIR = AVATAR_UPLOAD_ROOT / "users"
DOMAIN_AVATAR_DIR = AVATAR_UPLOAD_ROOT / "domains"

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
}
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024


def ensure_upload_dirs() -> None:
    USER_AVATAR_DIR.mkdir(parents=True, exist_ok=True)
    DOMAIN_AVATAR_DIR.mkdir(parents=True, exist_ok=True)


def _resolve_target_dir(scope: str) -> Path:
    if scope == "user":
        return USER_AVATAR_DIR
    if scope == "domain":
        return DOMAIN_AVATAR_DIR
    raise HTTPException(status_code=400, detail="Unsupported upload scope")


async def save_image_upload(file: UploadFile, *, scope: str) -> str:
    ensure_upload_dirs()

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported image extension")

    if file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image content type")

    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if len(payload) > MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="Image file is too large")

    target_dir = _resolve_target_dir(scope)
    filename = f"{uuid.uuid4().hex}{suffix}"
    save_path = target_dir / filename
    save_path.write_bytes(payload)

    return f"/uploads/avatars/{scope}s/{filename}"


def delete_uploaded_file(relative_path: str | None) -> None:
    if not relative_path or not relative_path.startswith("/uploads/"):
        return

    target_path = BASE_DIR.joinpath(*Path(relative_path.lstrip("/")).parts)
    try:
        resolved_target = target_path.resolve()
        resolved_root = UPLOAD_ROOT.resolve()
        if resolved_root in resolved_target.parents and resolved_target.is_file():
            resolved_target.unlink(missing_ok=True)
    except OSError:
        return

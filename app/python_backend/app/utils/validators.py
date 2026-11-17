from __future__ import annotations

import io
from typing import Tuple

from fastapi import HTTPException, UploadFile, status

from app.config import get_settings


settings = get_settings()


MAGIC_NUMBERS: Tuple[Tuple[bytes, str], ...] = (
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
)


def _detect_mime_magic(data: bytes) -> str | None:
    for magic, mime in MAGIC_NUMBERS:
        if data.startswith(magic):
            return mime
    return None


async def validate_upload_image(file: UploadFile) -> bytes:
    if file.content_type not in settings.allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG and PNG images are supported.",
        )

    raw = await file.read()
    size_mb = len(raw) / (1024 * 1024)
    if size_mb > settings.max_upload_size_mb:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image too large. Max {settings.max_upload_size_mb} MB.",
        )

    head = raw[:16]
    detected = _detect_mime_magic(head)
    if detected is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported or corrupted image file.",
        )

    # reset internal pointer for potential reuse
    file.file = io.BytesIO(raw)
    return raw


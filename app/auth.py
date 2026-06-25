from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from .settings import get_settings


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(api_key: str | None = Depends(api_key_header)) -> None:
    """Validate the X-API-Key header for protected endpoints."""

    settings = get_settings()
    if not api_key or api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )

import json
import logging
import time
import uuid
from collections.abc import AsyncIterator
from typing import Any

from fastapi import Body, Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse, StreamingResponse

from .auth import require_api_key
from .logging_config import setup_logging
from .schemas import AgentPendingResponse, HealthResponse
from .settings import get_settings

settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger("agent_api")

app = FastAPI(
    title="AI Travel Coordinator Agent API",
    description="Notion 모듈 1.8 기준 운영형 Agent API 서버 뼈대입니다.",
    version="0.1.0",
)


@app.middleware("http")
async def access_log_middleware(request: Request, call_next):
    """Attach a request ID and emit one structured JSON access log per request."""

    started_at = time.perf_counter()
    request_id = uuid.uuid4().hex[:12]
    request.state.request_id = request_id

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.exception(
            "request_failed",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "status_code": 500,
                "duration_ms": duration_ms,
            },
        )
        raise

    duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_completed",
        extra={
            "request_id": request_id,
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


@app.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    """Operational health check endpoint."""

    return HealthResponse(status="ok")


@app.post(
    "/chat",
    response_model=AgentPendingResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    dependencies=[Depends(require_api_key)],
)
async def chat(
    request: Request,
    payload: dict[str, Any] = Body(...),
) -> AgentPendingResponse:
    """Accept the future travel-agent request shape while agent code is still user-owned."""

    return AgentPendingResponse(
        detail=(
            "Travel agent implementation is intentionally pending. "
            "Fill app/agent.py, app/agents/*, and the request schema notes in app/schemas.py."
        ),
        request_id=getattr(request.state, "request_id", None),
    )


@app.post(
    "/chat/stream",
    dependencies=[Depends(require_api_key)],
)
async def chat_stream(
    request: Request,
    payload: dict[str, Any] = Body(...),
) -> StreamingResponse:
    """Streaming endpoint placeholder until the travel-agent stream is implemented."""

    async def pending_stream() -> AsyncIterator[str]:
        message = AgentPendingResponse(
            detail=(
                "Travel agent streaming is intentionally pending. "
                "Implement agent orchestration first, then yield partial schedule events here."
            ),
            request_id=getattr(request.state, "request_id", None),
        )
        yield json.dumps(message.model_dump(), ensure_ascii=False) + "\n"

    return StreamingResponse(
        pending_stream(),
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        media_type="application/x-ndjson",
    )

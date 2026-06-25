import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any


class JsonFormatter(logging.Formatter):
    """Format log records as single-line JSON for production log collectors."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        for key in (
            "request_id",
            "path",
            "method",
            "status_code",
            "duration_ms",
        ):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def setup_logging(level: str = "INFO") -> None:
    """Configure root logging once with a JSON stdout handler."""

    root_logger = logging.getLogger()
    root_logger.setLevel(level.upper())

    if any(getattr(handler, "_agent_api_handler", False) for handler in root_logger.handlers):
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler._agent_api_handler = True  # type: ignore[attr-defined]
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

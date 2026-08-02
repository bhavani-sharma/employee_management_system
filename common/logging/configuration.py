import json
import logging
import logging.config
from datetime import datetime, timezone
from typing import Any

_STANDARD_RECORD_KEYS = set(vars(logging.LogRecord("", 0, "", 0, "", (), None)).keys())


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "file": record.filename,
            "line": record.lineno,
            "function": record.funcName,
        }

        for key, value in vars(record).items():
            if key not in _STANDARD_RECORD_KEYS and key not in payload:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": "common.logging.configuration.JSONFormatter"},
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "handlers": ["default"],
        "level": "INFO",
    },
    "loggers": {
        # uvicorn's logging
        "app": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn": {"handlers": [], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": [], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": [], "level": "INFO", "propagate": False},
    },
}


def logging_configure() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)

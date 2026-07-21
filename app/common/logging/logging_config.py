import json
import logging
import logging.config
from datetime import datetime, timezone
from typing import Any, Dict


_STANDARD_RECORD_KEYS = set(vars(logging.LogRecord("", 0, "",0,"",(),None)).keys())

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp" : datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger" : record.name,
            "message" : record.getMessage(),
        }

        for key, value in vars(record).items():
            if key not in _STANDARD_RECORD_KEYS and key not in payload:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(payload, default=str)
    

LOGGING_CONFIG: Dict[str, Any] =  {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": "common.logging.logging_config.JSONFormatter"},
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
        # The app's own logger namespace (main, services, exception handlers, ...)
        "app": {"handlers": ["default"], "level": "INFO", "propagate": False},
        # Uvicorn's own loggers, reconfigured to use the same JSON handler
        # instead of their default colorized plain-text formatters.
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["default"], "level": "INFO", "propagate": False},
    },
}


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
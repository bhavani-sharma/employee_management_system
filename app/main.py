from fastapi import FastAPI
from app.common.data.base import Base
from app.common.data.database import engine
from app.endpoints import emp_endpoints
from app.endpoints import user_endpoints
from app.common.exceptions.exception_handlers import ExceptionHandlers
from app.common.logging.middleware import RequestLoggingMiddleware

from app.common.logging.logging_config import configure_logging

import logging

configure_logging()
logger = logging.getLogger("app")

Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Employee Management System")

app.add_middleware(RequestLoggingMiddleware)

exc = ExceptionHandlers()
exc.register(app)

app.include_router(user_endpoints.router)
app.include_router(emp_endpoints.router)

logger.info("applicaion_startup", extra={"event": "startup"})
from fastapi import FastAPI
from common.data.base import Base
from common.data.database import engine
from endpoints import emp_endpoints
from endpoints import user_endpoints
from common.exceptions.exception_handlers import ExceptionHandlers
from common.logging.middleware import RequestLoggingMiddleware
from dotenv import load_dotenv
from common.logging.logging_config import configure_logging

import logging
load_dotenv()
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
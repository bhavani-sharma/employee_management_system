import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_injector import InjectorMiddleware, RequestScopeOptions, attach_injector
from injector import Injector
from starlette_context.middleware import RawContextMiddleware

from common.data.base import Base
from common.data.database import engine
from common.exception.exception_handler import ExceptionHandlers
from common.injector.injector_configuration import create_injector
from common.logging.configuration import logging_configure
from common.logging.middleware import RequestLoggingMiddleware
from employee.endpoint import endpoint as employee_endpoint
from user.endpoint import endpoint as user_endpoint

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_startup", extra={"event": "startup"})
    Base.metadata.create_all(bind=engine)

    try:
        yield
    finally:
        engine.dispose()
        logger.info("application_shutdown", extra={"event": "shutdown"})


def create_app(injector: Injector | None = None) -> FastAPI:
    logging_configure()

    injector = injector or create_injector()

    app = FastAPI(title="Employee Management System", lifespan=lifespan)

    app.add_middleware(InjectorMiddleware, injector=injector)
    app.add_middleware(RawContextMiddleware)

    attach_injector(
        app,
        injector,
        RequestScopeOptions(enable_cleanup=True),
    )

    app.add_middleware(RequestLoggingMiddleware)
    ExceptionHandlers().register(app)

    app.include_router(user_endpoint.router)
    app.include_router(employee_endpoint.router)
    return app


app = create_app()

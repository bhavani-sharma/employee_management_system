from starlette_context import context

from user.application.model.model import CurrentUser


class RequestContext:
    _CURRENT_USER = "current_user"

    @staticmethod
    def set_current_user(user: CurrentUser) -> None:
        context[RequestContext._CURRENT_USER] = user

    @staticmethod
    def get_current_user() -> CurrentUser:
        user = context.get(RequestContext._CURRENT_USER)
        if user is None:
            raise RuntimeError("Current user has not been set")
        return context[RequestContext._CURRENT_USER]

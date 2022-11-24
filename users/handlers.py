"""Business logic"""
from django.http import HttpResponse


class BaseHandler:

    def __init__(self, request, *args, **kwargs):
        self.request = request

    def get_response(self, *args, **kwargs) -> HttpResponse:
        raise NotImplementedError


class ClientHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        pass


class TeacherHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        pass


class ManagerHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        pass


class HeadManagerHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        pass


class UserHandlerFactory:

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.handlers = {
            'Клиент': ClientHandler,
            'Преподаватель': TeacherHandler,
            'Менеджер': ManagerHandler,
            'Старший менеджер': HeadManagerHandler
        }
        self.args = args
        self.kwargs = kwargs

    def get_response(self, *args, **kwargs) -> HttpResponse:
        handler = self.handlers.get(self.request.user.role, None)(
            self.request, *self.args, **self.kwargs
        )
        if not handler:
            raise NotImplementedError

        return handler.get_response(*args, **kwargs)

"""Business logic"""
from django.http import HttpResponse
from django.shortcuts import render


class BaseHandler:

    def __init__(self, request, *args, **kwargs):
        self.request = request

    def get_response(self, *args, **kwargs) -> HttpResponse:
        raise NotImplementedError


class ClientHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:

        context = {
            'title': 'Профиль клиента'
        }
        return render(self.request, 'users/client_profile.html', context)


class TeacherHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        salary = (user.salary or 0) + len(user.lessons.all()) * (
            user.percent_salary or 0
        )
        context = {
            'title': 'Профиль клиента',
            'salary': salary
        }
        return render(self.request, 'users/client_profile.html', context)


class ManagerHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        salary = (user.salary or 0) + len(user.users.all()) * (
            user.percent_salary or 0
        )
        context = {
            'title': 'Профиль менеджера',
            'salary': salary,
        }
        return render(self.request, 'users/client_profile.html', context)


class HeadManagerHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        salary = (user.salary or 0) + len(user.users.all()) * (
            user.percent_salary or 0
        )
        context = {
            'title': 'Профиль старшего менеджера',
            'salary': salary,
        }
        return render(self.request, 'users/client_profile.html', context)


class UserHandlerFactory:

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.handlers = {
            'C': ClientHandler,
            'T': TeacherHandler,
            'M': ManagerHandler,
            'H': HeadManagerHandler
        }
        self.args = args
        self.kwargs = kwargs

    def get_response(self, *args, **kwargs) -> HttpResponse:
        handler_class = self.handlers.get(self.request.user.role, None)
        if not handler_class:
            raise NotImplementedError

        handler = handler_class(
            self.request, *self.args, **self.kwargs
        )
        return handler.get_response(*args, **kwargs)

"""Business logic"""
from django.http import HttpResponse
from django.shortcuts import render

from users.variables import links as links_list


class BaseHandler:

    def __init__(self, request, *args, **kwargs):
        self.request = request

    def get_response(self, *args, **kwargs) -> HttpResponse:
        raise NotImplementedError


class ClientHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        links = [links_list.get('courses')]

        context = {
            'title': 'Профиль клиента',
            'links': links
        }
        return render(self.request, 'users/client_profile.html', context)


class TeacherHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        links = [links_list.get('courses')]
        user = self.request.user
        salary = user.salary + len(user.lessons.all()) * user.percent_salary
        context = {
            'title': 'Профиль клиента',
            'links': links,
            'salary': salary
        }
        return render(self.request, 'users/client_profile.html', context)


class ManagerHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        links = [v for k, v in links_list.items() if k != 'managers']
        user = self.request.user
        salary = user.salary + len(user.users.all()) * user.percent_salary
        context = {
            'title': 'Профиль менеджера',
            'salary': salary,
            'links': links
        }
        return render(self.request, 'users/client_profile.html', context)


class HeadManagerHandler(BaseHandler):

    def get_response(self, *args, **kwargs) -> HttpResponse:
        pass


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

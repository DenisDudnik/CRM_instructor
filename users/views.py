# from django.shortcuts import render
from django.http import HttpResponse

from users.handlers import UserHandlerFactory

# Create your views here.


def user_profile(request) -> HttpResponse:
    """Connector for rendering users profile page"""

    factory = UserHandlerFactory(request)
    return factory.get_response()

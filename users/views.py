from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import LoginForm
from users.handlers import UserHandlerFactory


def login(request) -> HttpResponse:
    """Login user controller"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-detail'))

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('user-detail'))
    form = LoginForm()
    context = {
        'title': 'Вход',
        'form': form
    }
    return render(request, 'users/login.html', context)


def logout(request):
    """Logout controller"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


@login_required
def user_profile(request) -> HttpResponse:
    """Connector for rendering users profile page"""
    if request.user.is_authenticated:
        factory = UserHandlerFactory(request)
        return factory.get_response()
    else:
        return HttpResponseRedirect(reverse('auth:login'))

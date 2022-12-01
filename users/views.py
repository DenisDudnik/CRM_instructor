from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from users.forms import LoginForm, UserEditForm
from users.handlers import UserHandlerFactory
from users.models import User
from users.variables import links


def placeholder(request):
    pass


def login(request) -> HttpResponse:
    """Login user controller"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_profile'))

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('user_profile'))
    form = LoginForm()
    context = {
        'title': 'Вход',
        'form': form,
        'button': 'Войти'
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


@login_required
def profile_edit(request) -> HttpResponse:
    """Edit profile"""
    title = "Редактирование профиля"
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_profile'))
    else:
        form = UserEditForm(instance=request.user)
    context = {
        'title': title,
        'form': form,
        'button': 'Сохранить'
    }
    return render(request, 'users/login.html', context)


class ClientsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        if self.request.META['PATH_INFO'] == '/clients_list/':
            if self.request.user.role == 'M':
                return User.objects.filter(
                    role='C', manager__id=self.request.user.id
                )
            elif self.request.user.role == 'H':
                return User.objects.filter(
                    role='C'
                )
            else:
                return []
        elif self.request.META['PATH_INFO'] == '/teachers_list/':
            if self.request.user.role in ('M', 'H'):
                return User.objects.filter(
                    role='T'
                )
            return []

    def get_context_data(self, **kwargs):
        print(self.request.META['PATH_INFO'])
        context = super(ClientsListView, self).get_context_data(**kwargs)
        context['title'] = 'Список клиентов'
        context['links'] = [v for k, v in links.items() if k != 'managers']
        return context

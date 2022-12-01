from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from users.forms import LoginForm, UserCreateForm, UserEditForm
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


@login_required
def create_user(request):
    """Create new user"""
    title = 'Добавление пользователя'
    if request.method == 'POST':
        form = UserCreateForm(request.POST, manager=request.user)
        if form.is_valid():
            form.save()
            if form.data.get('role') == 'C':
                rev = 'clients'
            elif form.data.get('role'):
                rev = 'teachers'
            else:
                rev = 'managers'
            return HttpResponseRedirect(reverse(rev))
    else:
        form = UserCreateForm(manager=request.user)
        if request.user.role == 'H':
            links_list = [v for k, v in links.items()]
        else:
            links_list = [v for k, v in links.items() if k != 'managers']
        context = {
            'title': title,
            'form': form,
            'links': links_list,
            'button': 'Сохранить'
        }
        return render(request, 'users/login.html', context)


class ClientsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'clients'

    titles = {
        '/clients_list/': 'Список клиентов',
        '/teachers_list/': 'Список тренеров',
        '/managers_list/': 'Список менеджеров'
    }

    def get_links(self):
        if self.request.user.role in ('C', 'T'):
            return [links.get('courses')]
        elif self.request.user.role == 'M':
            return [v for k, v in links.items() if k != 'managers']
        else:
            return [v for v in links.values()]

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
        elif self.request.META['PATH_INFO'] == '/managers_list/':
            if self.request.user.role == 'H':
                return User.objects.filter(role__in=['M', 'H'])
            return []

    def get_context_data(self, **kwargs):
        context = super(ClientsListView, self).get_context_data(**kwargs)
        context['title'] = self.titles.get(self.request.META['PATH_INFO'], '')
        context['links'] = self.get_links()
        return context

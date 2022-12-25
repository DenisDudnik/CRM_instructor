from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from users.forms import (LoginForm, ManagerUserEditForm, UserEditForm,
                         UserManagerCreateForm)
from users.handlers import UserHandlerFactory
from users.models import User
from users.tasks import send_mail


def placeholder(request) -> HttpResponse:
    return render(request, 'users/404.html', {'title': '404'})


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
        'button': 'Войти',
        'button_2': 'Сбросить пароль',
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
        'button': 'Сохранить',
        'back': reverse('user_profile')
    }
    return render(request, 'users/form.html', context)


@login_required
def create_user(request, role: str):
    """Create new user"""
    title = 'Добавление пользователя'
    context = {
        'title': title,
        'button': 'Сохранить',
        'back': request.META.get('HTTP_REFERER')
    }
    if request.method == 'POST':
        form = UserManagerCreateForm(
            request.POST, manager=request.user, role=role)
        if form.is_valid():
            user = form.save()
            if form.data['email']:

                email_context = {
                    'user': user,
                    'manager': User.objects.get(id=request.user.id),
                    'domain': settings.SERVER_URI
                }

                send_mail(
                    user,
                    'users/send_mail_user_register.html',
                    f"{user.first_name}, вы зарегистрированы в crm_instructor!",
                    email_context)

            if role == 'C':
                rev = 'clients'
            elif role == 'T':
                rev = 'teachers'
            else:
                rev = 'managers'
            return HttpResponseRedirect(reverse(rev))
    else:
        form = UserManagerCreateForm(manager=request.user, role=role)
    context['form'] = form
    return render(request, 'users/form.html', context)


class ClientsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'clients'

    titles = {
        '/clients_list/': ['Список клиентов', 'C', True, True],
        '/teachers_list/': ['Список тренеров', 'T', False, True],
        '/managers_list/': ['Список менеджеров', 'M', False, True]
    }

    def get_queryset(self):
        if self.request.META['PATH_INFO'] == '/clients_list/':
            if self.request.user.role == 'M':
                return User.objects.filter(
                    role='C', manager__id=self.request.user.id
                )
            elif self.request.user.role == 'H':
                return User.objects.filter(
                    role='C'
                ).all()
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
        title, role, status, comment = self.titles.get(
            self.request.META['PATH_INFO'])
        context['title'] = title
        context['role'] = role
        context['show_status'] = status
        context['show_comment'] = comment
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'item'


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/form.html'
    extra_context = {
        'title': 'редактирование пользователя',
        'button': 'Сохранить',
    }
    form_class = ManagerUserEditForm
    context_object_name = 'item'

    urls = {
        'C': reverse_lazy('clients'),
        'T': reverse_lazy('teachers'),
        'M': reverse_lazy('managers'),
    }

    def get_success_url(self):
        return self.urls.get(self.object.role)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back'] = self.get_success_url()
        return context


class UserPasswordEditView(PasswordChangeView):
    """Change password form"""
    model = User
    template_name = 'users/form.html'
    extra_context = {
        'title': 'Смена пароля',
        'button': 'Сохранить',
    }
    context_object_name = 'item'


class UserPasswordResetView(PasswordResetView):
    """Initialize password reset. Enter corresponding e-mail to receive reset link"""
    template_name = 'users/password-reset/password_reset_form.html',
    subject_template_name = 'users/password-reset/password_reset_subject.txt',
    email_template_name = 'users/password-reset/password_reset_email.html',
    extra_context = {
        'title': 'Сброс пароля',
        'button': 'Сбросить пароль',
    }
    context_object_name = 'item'


class UserPasswordResetDoneView(PasswordResetDoneView):
    """Automatically displays after submitting an e-mail"""
    template_name = 'users/password-reset/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """This link is emailed to the user. Here token is validated against user data."""
    template_name = 'users/password-reset/password_reset_confirm.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """Page Display after successful Password Reset."""
    template_name = 'users/password-reset/password_reset_complete.html'

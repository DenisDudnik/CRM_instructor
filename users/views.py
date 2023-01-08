from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
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
        else:
            return HttpResponseRedirect(reverse('auth:password_reset'))
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

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.POST = None
        self.method = None

    @csrf_protect
    def password_reset(request, is_admin_site=False,
                       template_name='/users/password-reset/password_reset_form.html',
                       email_template_name='users/password-reset/password_reset_email.html',
                       subject_template_name='users/password-reset/password_reset_subject.txt',
                       password_reset_form=PasswordResetForm,
                       token_generator=default_token_generator,
                       post_reset_redirect=None,
                       from_email=None,
                       extra_context=None):
        if post_reset_redirect is None:
            post_reset_redirect = reverse('auth:password_reset_done')
        else:
            post_reset_redirect = resolve_url(post_reset_redirect)
        if request.method == "POST":
            form = password_reset_form(request.POST)
            if form.is_valid():
                opts = {
                    'token_generator': token_generator,
                    'from_email': from_email,
                    'email_template_name': email_template_name,
                    'subject_template_name': subject_template_name,
                    'request': request,
                }
                if is_admin_site:
                    opts = dict(opts, domain_override=request.get_host())
                form.save(**opts)
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = password_reset_form()
        context = {
            'form': form,
        }
        if extra_context is not None:
            context.update(extra_context)
        return TemplateResponse(request, template_name, context)

    def get_host(self):
        pass


class UserPasswordResetDoneView(PasswordResetDoneView):
    """Automatically displays after submitting an e-mail"""
    def password_reset_done(request,
                            template_name='users/password-reset/password_reset_done.html',
                            current_app=None, extra_context=None):
        context = {}
        if extra_context is not None:
            context.update(extra_context)
        return TemplateResponse(request, template_name, context)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """This link is emailed to the user. Here token is validated against user data."""

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.POST = None
        self.method = None

    @sensitive_post_parameters()
    @never_cache
    def password_reset_confirm(request, uidb64=None, token=None,
                               template_name='users/password-reset/password_reset_confirm.html',
                               token_generator=default_token_generator,
                               set_password_form=SetPasswordForm,
                               post_reset_redirect=None,
                               current_app=None, extra_context=None):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        user = get_user_model()
        assert uidb64 is not None
        assert token is not None
        if post_reset_redirect is None:
            post_reset_redirect = reverse('auth:password_reset_complete')
        else:
            post_reset_redirect = resolve_url(post_reset_redirect)
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = user.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            valid_link = True
            if request.method == 'POST':
                form = set_password_form(user, request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(post_reset_redirect)
            else:
                form = set_password_form(None)
        else:
            valid_link = False
            form = None
        context = {
            'form': form,
            'validlink': valid_link,
        }
        if extra_context is not None:
            context.update(extra_context)
        return TemplateResponse(request, template_name, context)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """Page Display after successful Password Reset."""
    def password_reset_complete(request,
                                template_name='users/password-reset/password_reset_complete.html',
                                current_app=None, extra_context=None):
        context = {
            'login_url': resolve_url(settings.LOGIN_URL)
        }
        if extra_context is not None:
            context.update(extra_context)
        return TemplateResponse(request, template_name, context)

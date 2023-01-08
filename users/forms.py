"""Users forms module"""
import random
from string import ascii_letters

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms.models import ModelForm
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.models import User


class LoginForm(AuthenticationForm):
    """Form for users login"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-field'

    class Meta:
        model = User
        fields = ('username', 'password')


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")


class UserCreateForm(ModelForm):
    _fields = {
        'C': ("salary", "percent_salary",),
        'T': ("status", "manager"),
        'M': ("status", "manager")
    }

    _roles = {
        'C': User.CLIENT,
        'T': User.TEACHER,
        'M': User.MANAGER,
    }
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, role: str, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self._fields.get(role)
        for field in fields:
            self.fields.pop(field)
        if "manager" in self.fields.keys():
            self.fields['manager'].queryset = User.objects.filter(
                role__in=[User.MANAGER, User.HEAD_MANAGER])
        self.fields['role'].initial = self._roles.get(role)
        self.fields['role'].disabled = True

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone",
            "role",
            "manager",
            "salary",
            "percent_salary",
            "status",
            "comment"
        )


class UserManagerCreateForm(UserCreateForm):

    def __init__(self, *args, **kwargs):
        manager = kwargs.pop('manager')
        super(UserManagerCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label == 'Персональный менеджер':
                field.queryset = User.objects.filter(pk=manager.pk)
            if field.label != 'Комментарий':
                field.widget.attrs['required'] = True

    @staticmethod
    def generate_username_or_password():
        username = ''
        for i in range(20):
            username += random.choice(ascii_letters)
        return username

    def save(self, commit=True):
        user = User(**self.cleaned_data)
        if user.username == '':
            user.username = self.generate_username_or_password()
        if user.password == '':
            user.password = self.generate_username_or_password()
        password = forms.CharField(widget=forms.PasswordInput())
        user.set_password(str(password))
        user.save()
        return user


class ManagerUserEditForm(UserChangeForm):
    _fields = {
        'C': ("salary", "percent_salary",),
        'T': ("status", "manager"),
        'M': ("status", "manager")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self._fields.get(self.instance.role)
        for field in fields:
            self.fields.pop(field)
        manager = self.fields.get('manager')
        if manager:
            manager.queryset = User.objects.filter(
                role__in=[User.MANAGER, User.HEAD_MANAGER]
            )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "manager",
            "salary",
            "percent_salary",
            "status",
            "comment"
        )


class HTMLPasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

    def save(self, domain_override=None,
             subject_template_name='users/password-reset/password_reset_subject.txt',
             email_template_name='users/password-reset/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        user = get_user_model()
        email = self.cleaned_data["email"]
        active_users = user.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            subject = loader.render_to_string(subject_template_name, c)
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])

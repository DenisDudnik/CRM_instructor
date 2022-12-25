"""Users forms module"""
import random
from string import ascii_letters

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.forms.models import ModelForm

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

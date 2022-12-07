"""Users forms module"""
import random
from string import ascii_letters

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

    def __init__(self, *args, role: str = 'C', **kwargs):

        choices = {
            'C': ('C', 'Клиент'),
            'T': ('T', 'Преподаватель'),
            'M': ('M', 'Менеджер')
        }

        manager = kwargs.pop('manager')
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label == 'Роль':
                field.choices = [choices.get(role)]
            if field.label == 'Персональный менеджер':
                field.queryset = User.objects.filter(pk=manager.pk)
            field.widget.attrs['required'] = True

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone',
            'role',
            'manager'
        )

    @staticmethod
    def generate_username_or_password():
        username = ''
        for i in range(20):
            username += random.choice(ascii_letters)
        return username

    def save(self, commit=True):
        user = User(**self.cleaned_data)
        user.username = self.generate_username_or_password()
        user.set_password(self.generate_username_or_password())
        user.save()
        return user

"""Users forms module"""

from django.contrib.auth.forms import AuthenticationForm

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

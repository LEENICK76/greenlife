from enum import Enum

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    def _init_(self, *args, **kwargs):
        super(RegisterForm, self)._init_(*args, **kwargs)

    class AccountType(Enum):
        CUSTOMER = 'CUSTOMER',
        FARMER = 'FARMER'

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-row txt-input',
            'placeholder': 'Enter your name'
        }
    ))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-row txt-input',
            'placeholder': 'Enter your name'
        }
    ))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-row txt-input',
            'placeholder': 'Enter your name'
        }
    ))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'input-text',
            'placeholder': 'Enter your email'
        }
    ))
    number = forms.IntegerField()
    # account_type = forms.ChoiceField(choices=AccountType.choices(), widget=forms.Select(
    #     attrs={'class': 'input-text nice-select orderby',
    #            'style': 'color:red'
    #            }))

    class Meta:
        model = User
        fields = ('username', 'email', 'number', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    def _init_(self, *args, **kwargs):
        super(LoginForm, self)._init_(*args, **kwargs)

    email = forms.EmailField()
    password = forms.PasswordInput()


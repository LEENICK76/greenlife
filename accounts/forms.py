from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    def _init_(self, *args, **kwargs):
        super(RegisterForm, self)._init_(*args, **kwargs)

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    number = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'number', 'password1', 'password2')
        

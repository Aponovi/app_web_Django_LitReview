# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms


#
#
# class SignupForm(UserCreationForm):
#
#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2']
#
#         }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')

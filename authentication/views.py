from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View, CreateView, ListView

from . import forms
from .forms import SignUpForm


class SignUp_page(generic.CreateView):
    template_name = 'authentication/subscribe.html'
    sucess_url = reverse_lazy('login')
    form_class = SignUpForm


class LoginPageView(views.LoginView):
    template_name = 'authentication/login.html'
    next_page = reverse_lazy('flux')
    form_class = forms.LoginForm

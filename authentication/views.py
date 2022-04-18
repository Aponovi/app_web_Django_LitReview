from django.contrib.auth import views, logout
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignUpForm


class SignUp_page(generic.CreateView):
    template_name = 'authentication/subscribe.html'
    success_url = reverse_lazy('authentication:home')
    form_class = SignUpForm


class LoginPageView(views.LoginView):
    template_name = 'authentication/home.html'
    next_page = reverse_lazy('forum:flux')


class LogoutPageView(views.LogoutView):
    next_page = reverse_lazy('authentication:home')

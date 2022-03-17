from django.urls import path
from . import views

urlpatterns = [
    path('inscription', views.signup_page, name='subscribe'),
    path('accueil', views.LoginPageView.as_view(), name='login'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('inscription', views.SignUp_page.as_view(), name='subscribe'),
    path('accueil', views.LoginPageView.as_view(), name='login'),
]
from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('inscription', views.SignUp_page.as_view(), name='subscribe'),
    path('', views.LoginPageView.as_view(), name='login'),
]

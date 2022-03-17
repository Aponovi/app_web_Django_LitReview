from django.urls import path
from . import views

urlpatterns = [
    path('flux', views.flux_page, name='flux'),
]
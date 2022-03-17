from django.urls import path
from . import views

urlpatterns = [
    path('flux', views.flux_page, name='flux'),
    path('abonnements', views.follow_page, name='follow'),
    path('ticket', views.ticket_page, name='ticket'),
    path('critique', views.review_page, name='review'),
    path('réponse', views.response_page, name='response'),
    path('posts', views.posts_page, name='posts'),
]
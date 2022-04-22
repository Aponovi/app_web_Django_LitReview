from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('flux', views.TicketsList.as_view(), name='flux'),
    path('abonnements', views.follow_page, name='follow'),
    path('ticket', views.TicketCreation.as_view(), name='ticket'),
    path('critique', views.review_page, name='review'),
    path('réponse', views.response_page, name='response'),
    path('posts', views.posts_page, name='posts'),
]

from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('flux', views.TicketsList.as_view(), name='flux'),
    path('abonnements', views.follow_page, name='follow'),
    path('ticket/<int:pk>/', views.TicketUpdate.as_view(), name='ticket'),
    path('ticket/delete/<int:pk>/', views.TicketDelete.as_view(), name='ticket_delete'),
    path('ticket', views.TicketCreation.as_view(), name='ticket'),
    path('critique', views.ReviewCreation.as_view(), name='review'),
    path('critique/<int:id_ticket>/', views.ReviewCreation.as_view(), name='review'),
    path('réponse', views.response_page, name='response'),
    path('posts', views.PostsPage.as_view(), name='posts'),
]

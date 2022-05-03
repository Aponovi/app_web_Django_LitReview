from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('flux', views.TicketsListView.as_view(), name='flux'),
    path('abonnements', views.follow_page, name='follow'),
    path('ticket/<int:pk>/', views.TicketUpdateView.as_view(), name='ticket'),
    path('ticket/delete/<int:pk>/', views.TicketDeleteView.as_view(), name='ticket_delete'),
    path('ticket', views.TicketCreationView.as_view(), name='ticket_create'),
    path('critique', views.ReviewCreationView.as_view(), name='review_create'),
    path('critique/<int:id_ticket>/', views.ReviewResponseView.as_view(), name='review_response'),
    path('posts', views.PostsPageView.as_view(), name='posts'),
]

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, CreateView, ListView

# Create your views here.
from forum.models import Ticket


def flux_page(request):
    return HttpResponse('<h1>Hello, world!</h1>')


def follow_page(request):
    return HttpResponse('<h1>Qui je suis! Et surtout qui me suis?</h1>')


class LST(ListView):
    template_name = ''
    context_object_name = 'tickets'
    queryset = Ticket.objects.all()


def ticket_page(request):
    return HttpResponse('<h1>créer un ticket</h1>')


def review_page(request):
    return HttpResponse('<h1>créer une critique</h1>')


def response_page(request):
    return HttpResponse('<h1>répondre à un ticket</h1>')


def posts_page(request):
    return HttpResponse('<h1>mes posts</h1>')

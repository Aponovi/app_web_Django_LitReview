from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def flux_page(request):
    return HttpResponse('<h1>Hello, world!</h1>')


def follow_page(request):
    return HttpResponse('<h1>Qui je suis! Et surtout qui me suis?</h1>')


def ticket_page(request):
    return HttpResponse('<h1>créer un ticket</h1>')


def review_page(request):
    return HttpResponse('<h1>créer une critique</h1>')


def response_page(request):
    return HttpResponse('<h1>répondre à un ticket</h1>')


def posts_page(request):
    return HttpResponse('<h1>mes posts</h1>')

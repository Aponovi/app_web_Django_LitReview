from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView

# Create your views here.
from forum.models import Ticket
from . import forms


def flux_page(request):

    return HttpResponse('<h1>Hello, world!</h1>')


def follow_page(request):
    return HttpResponse('<h1>Qui je suis! Et surtout qui me suis?</h1>')


class LST(ListView):
    template_name = 'forum/flux.html'
    context_object_name = 'tickets'
    queryset = Ticket.objects.order_by('-time_created')
    paginate_by = '5'


class TicketCreation(LoginRequiredMixin, CreateView):
    template_name = 'forum/ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('forum:flux')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def review_page(request):
    return HttpResponse('<h1>créer une critique</h1>')


def response_page(request):
    return HttpResponse('<h1>répondre à un ticket.html</h1>')


def posts_page(request):
    return HttpResponse('<h1>mes posts</h1>')

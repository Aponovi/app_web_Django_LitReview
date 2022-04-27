from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView, UpdateView, DeleteView

# Create your views here.
from forum.models import Ticket
from . import forms


def follow_page(request):
    return HttpResponse('<h1>Qui je suis! Et surtout qui me suis?</h1>')


class TicketsList(LoginRequiredMixin, ListView):
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


class ReviewCreation(LoginRequiredMixin, CreateView):
    template_name = 'forum/review.html'
    form_class = forms.ReviewForm
    success_url = reverse_lazy('forum:flux')


class TicketUpdate(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ['title', 'description', 'image']
    template_name = 'forum/ticket_update.html'
    success_url = reverse_lazy('forum:flux')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TicketDelete(LoginRequiredMixin,  DeleteView):
    model = Ticket
    template_name = 'forum/ticket_delete.html'
    success_url = reverse_lazy('forum:flux')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def response_page(request):
    return HttpResponse('<h1>répondre à un ticket.html</h1>')


class PostsPage(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'forum/posts.html'
    context_object_name = 'tickets'

 #   user = User.objects.all().prefetch_related('ticket_set', 'ticket_set__review_set')
    queryset = Ticket.objects.filter(user__username=User.username).order_by('-time_created')
    paginate_by = '10'


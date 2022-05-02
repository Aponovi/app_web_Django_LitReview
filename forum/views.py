from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

# Create your views here.
from forum.models import Ticket, Review
from . import forms


def follow_page(request):
    return HttpResponse('<h1>Qui je suis! Et surtout qui me suis?</h1>')


class TicketsListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'forum/flux.html'
    context_object_name = 'tickets'
    ordering = ['-time_created']
#    queryset = Ticket.objects.order_by('-time_created')
    paginate_by = '5'


class TicketCreationView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'forum/ticket_create.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('forum:flux')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewCreationView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'forum/review.html'
    form_class = forms.ReviewForm
    success_url = reverse_lazy('forum:flux')

    _ticket = None

    @property
    def ticket(self):
        if self._ticket is None:
            self._ticket = get_object_or_404(Ticket.objects.all(), id=self.kwargs['id_ticket'])
        return self._ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.ticket
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ticket = self.ticket
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = forms.TicketForm
    template_name = 'forum/ticket_update.html'
    success_url = reverse_lazy('forum:flux')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'forum/ticket_delete.html'
    success_url = reverse_lazy('forum:flux')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def response_page(request):
    return HttpResponse('<h1>répondre à un ticket_create.html</h1>')


class PostsPageView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'forum/posts.html'
    context_object_name = 'tickets'
    paginate_by = '10'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-time_created')

#    user = User.objects.all().prefetch_related('ticket_set', 'ticket_set__review_set')

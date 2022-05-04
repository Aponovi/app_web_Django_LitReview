from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.forms import inlineformset_factory

# Create your views here.
from forum.models import Ticket, Review
from . import forms
from .forms import TicketForm, ReviewForm


def follow_page(request):
    return HttpResponse('<h1>Qui je suis! Et surtout qui me suis?</h1>')


class TicketsListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'forum/flux.html'
    context_object_name = 'tickets'
    paginate_by = '5'

    def get_context_data(self, **kwargs):
        tickets = Ticket.objects.all().annotate(content_type=Value("TICKET", CharField()))
        reviews = Review.objects.all().annotate(content_type=Value("REVIEW", CharField()))

        context = super().get_context_data(**kwargs)
        context['feeds'] = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created,
                                  reverse=True)

        return context


class TicketCreationView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'forum/ticket_create.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('forum:flux')

    def form_valid(self, form):
        form.instance.user = self.request.user
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


class ReviewResponseView(LoginRequiredMixin, CreateView):
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


class ReviewCreationView(LoginRequiredMixin, TemplateView):
    template_name = 'forum/review_create.html.'
    success_url = reverse_lazy('forum:flux')
    form_review = ReviewForm()
    form_ticket = TicketForm()

    def post(self, request, *args, **kwargs):
        form_review = ReviewForm(request.POST, request.FILES, prefix="review")
        form_ticket = TicketForm(request.POST, request.FILES, prefix="ticket")

        if form_review.is_valid() and form_ticket.is_valid():
            ticket = form_ticket.save(commit=False)
            form_ticket.instance.user = self.request.user
            ticket.save()
            review = form_review.save(commit=False)
            form_review.instance.user = self.request.user
            review.ticket = form_ticket.save()
            review.save()
            return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        form_ticket = TicketForm(prefix="ticket")
        form_review = ReviewForm(prefix="review")
        return {"form_ticket": form_ticket, "form_review": form_review}

    def get_success_url(self):
        return reverse_lazy('forum:flux')

    # def get_queryset(self):
    #     return self.t
    #         User.objects.all().prefetch_related('ticket_set', 'ticket_set__review_set')
    #
    #    user = User.objects.all().prefetch_related('ticket_set', 'ticket_set__review_set')


class PostsPageView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'forum/posts.html'
    context_object_name = 'tickets'
    paginate_by = '10'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-time_created')

#    user = User.objects.all().prefetch_related('ticket_set', 'ticket_set__review_set')

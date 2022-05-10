from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

from forum.models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, UserFollowsForm


# user = User.objects.all().prefetch_related('ticket_set', 'ticket_set__review_set')

class TicketsListView(LoginRequiredMixin, ListView):
    # Feed the flux page
    model = Ticket
    template_name = 'forum/flux.html'
    context_object_name = 'tickets'

    def get_context_data(self, **kwargs):
        # Get users.id followed by request.user
        followed_users_id = UserFollows.objects.filter(
            user=self.request.user
        ).values_list("followed_user_id", flat=True)

        # Get reviews make by user followed
        reviews_followed_users = (
            Review.objects.filter(
                Q(user__in=followed_users_id) | Q(user=self.request.user.id)
            ).select_related()
        ).annotate(content_type=Value("REVIEW", CharField()))

        # Get tickets make by user followed
        tickets_followed_users = (
            Ticket.objects.filter(
                Q(user__in=followed_users_id) | Q(user=self.request.user.id)
            ).select_related()
        ).annotate(content_type=Value("TICKET", CharField()))

        # Get users.id who follow request.user
        following_users_id = UserFollows.objects.filter(
            followed_user=self.request.user
        ).values_list("user_id", flat=True)

        # Get reviews make by them for request.user tickets
        reviews_following_users = (
            Review.objects.filter(
                Q(user__in=following_users_id) & Q(ticket__user=self.request.user.id)
            )
                .select_related()
                .annotate(content_type=Value("REVIEW", CharField()))
        )

        context = super().get_context_data(**kwargs)
        context['feeds'] = sorted(chain(reviews_followed_users,
                                        tickets_followed_users,
                                        reviews_following_users, ), key=lambda instance: instance.time_created,
                                  reverse=True)

        return context


class PostsPageView(LoginRequiredMixin, ListView):
    # Display tickets and reviews of logged in user only
    model = Ticket
    template_name = 'forum/posts.html'
    context_object_name = 'tickets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = Ticket.objects.filter(user=self.request.user).order_by('-time_created').annotate(
            content_type=Value("TICKET", CharField()))
        reviews = Review.objects.filter(user=self.request.user).order_by('-time_created').annotate(
            content_type=Value("REVIEW", CharField()))
        context['feeds'] = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created,
                                  reverse=True)

        return context


class TicketCreationView(LoginRequiredMixin, CreateView):
    # Create a ticket
    model = Ticket
    template_name = 'forum/ticket_create.html'
    form_class = TicketForm
    success_url = reverse_lazy('forum:flux')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    # Edit a ticket
    model = Ticket
    form_class = TicketForm
    template_name = 'forum/ticket_update.html'
    success_url = reverse_lazy('forum:flux')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    # Delete a ticket
    model = Ticket
    template_name = 'forum/ticket_delete.html'
    success_url = reverse_lazy('forum:flux')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ReviewResponseView(LoginRequiredMixin, CreateView):
    # Create a review in response to a ticket
    model = Review
    template_name = 'forum/review.html'
    form_class = ReviewForm
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
    # Create a review and a ticket in one go
    template_name = 'forum/review_create.html.'
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


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    # Edit a review
    model = Review
    form_class = ReviewForm
    template_name = 'forum/review_update.html'
    success_url = reverse_lazy('forum:flux')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    # Delete a review
    model = Review
    template_name = 'forum/review_delete.html'
    success_url = reverse_lazy('forum:flux')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class FollowCreationView(LoginRequiredMixin, CreateView):
    # Allowed follows and display lists of followers and followed
    model = UserFollows
    template_name = 'forum/abonnements.html'
    form_class = UserFollowsForm
    success_url = reverse_lazy('forum:follow')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_following = UserFollows.objects.all().select_related()
        user_followed = UserFollows.objects.all().select_related()

        context["current_user"] = self.request.user
        context["following_users"] = sorted(
            user_following,
            key=lambda user: user.user.username,
            reverse=False,
        )
        context["followed_users"] = sorted(
            user_followed,
            key=lambda user: user.followed_user.username,
            reverse=False,
        )
        return context


class FollowDeleteView(LoginRequiredMixin, DeleteView):
    # Delete the followed
    model = UserFollows
    template_name = 'forum/désabonnement.html'
    success_url = reverse_lazy('forum:follow')

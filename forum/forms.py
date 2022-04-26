from django.forms import ModelForm

from . import models


class TicketForm(ModelForm):
    model = models.Ticket

    class Meta:
        model = models.Ticket
        fields = ('title', 'description', 'image')


class ReviewForm(ModelForm):
    model = models.Review

    class Meta:
        model = models.Review
        fields = ('headline', 'rating', 'body')

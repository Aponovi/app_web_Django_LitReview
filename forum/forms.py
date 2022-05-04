from django.forms import ModelForm
from django import forms
from . import models


class TicketForm(ModelForm):
    class Meta:
        model = models.Ticket
        fields = ('title', 'description', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            #            'image': forms.ImageField(attrs={'class': 'form-control'}),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = models.Review
        fields = ('headline', 'rating', 'body')

        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            #           'rating': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

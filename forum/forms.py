from django.contrib.auth.forms import UserModel
from django.forms import ModelForm
from django import forms
from forum.models import Ticket, Review, UserFollows


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')

        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget = forms.RadioSelect(choices=self.Meta.model.RATING_CHOICES)


class UserFollowsForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = [
            'followed_user',
        ]
    followed_user = forms.ModelChoiceField(
        queryset=None,
        label="Suivre l'utilisateur :",
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['followed_user'].queryset = UserModel.objects.exclude(username=user.username)


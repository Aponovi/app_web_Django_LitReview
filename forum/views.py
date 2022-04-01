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
    template_name = ''
    context_object_name = 'tickets'
    queryset = Ticket.objects.all()


class TicketCreation(LoginRequiredMixin, CreateView):
    template_name = 'forum/ticket.html'
    form_class = forms.TicketForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.instance.user = self.request.user
        if form.is_valid():
            ticket = Ticket(title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            image=form.cleaned_data['image'],
                            user=request.user,
                            )
            ticket.save()
            return reverse_lazy('flux')
        else:
            return render(request, 'forum/ticket.html', {
                'form': form
            })



def review_page(request):
    return HttpResponse('<h1>créer une critique</h1>')


def response_page(request):
    return HttpResponse('<h1>répondre à un ticket.html</h1>')


def posts_page(request):
    return HttpResponse('<h1>mes posts</h1>')

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from photoshare import utils
from users.forms import SignUpForm


# Create your views here.
@utils.anonymous_required
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return HttpResponseRedirect(reverse('index'))

        return render(request, 'users/signup.html', {'form': form})

    return render(request, 'users/signup.html', {'form': SignUpForm()})


@utils.anonymous_required
def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return HttpResponseRedirect(reverse('index'))

        return render(request, 'users/login.html', {'form': form})


    return render(request, 'users/login.html', {'form': AuthenticationForm()})


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

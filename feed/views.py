from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User, Posts

# Create your views here.
@login_required
def index(request):
    return render(request, 'feed/index.html')


@login_required
def profile(request):
    return render(request, 'feed/profile.html')
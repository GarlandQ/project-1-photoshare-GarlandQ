from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Posts
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    return render(request, "feed/index.html")


@login_required
def profile(request):
    return render(request, "feed/profile.html")


@login_required
def editprofile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "feed/editprofile.html", context)
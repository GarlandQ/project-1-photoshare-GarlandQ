from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Post
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView

# Home page with posts
@login_required
def index(request):
    context = {"posts": Post.objects.all()}
    return render(request, "feed/index.html", context)


class PostListView(ListView):
    model = Post
    template_name = "feed/index.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    fields = ["image", "description"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "feed/editprofile.html", context)
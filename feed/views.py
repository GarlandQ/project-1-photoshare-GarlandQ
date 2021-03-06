from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment
from users.forms import UserUpdateForm, ProfileUpdateForm
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

# Home page with posts
@login_required
def index(request):
    context = {"posts": Post.objects.all()}
    return render(request, "feed/index.html", context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "feed/index.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(post=self.get_object()).order_by(
            "-created_date"
        )
        data["comments"] = comments_connected
        data["comment_form"] = CommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(
            content=request.POST.get("content"),
            owner=self.request.user,
            post=self.get_object(),
        )
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["image", "description"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["image", "description"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Test to see if the user updating their post is the actual user and not someone else
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    # Test to see if the user updating their post is the actual user and not someone else
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "feed/user_profile.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, username=self.kwargs.get("username"))
        context["Users_Profile"] = Profile.objects.all()
        return context


# @login_required
# def profile(request):
#     return render(request, "feed/profile.html")


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
            return redirect("user-profile", username=request.user.username)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "feed/editprofile.html", context)


# class CommentListView(LoginRequiredMixin, ListView):
#     model = Comment
#     template_name = "feed/post_detail.html"
#     context_object_name = "comments"


# class CommentDetailView(LoginRequiredMixin, DetailView):
#     model = Comment


# class CommentCreateView(LoginRequiredMixin, CreateView):
#     model = Comment
#     fields = ["content"]

#     def form_valid(self, form):
#         # post = get_object_or_404(Post, pk=id) # Uncommenting this line gives error: Field 'id' expected a number but got <built-in function id>.
#         form.instance.owner = self.request.user
#         # form.instance.post = post
#         return super().form_valid(form)

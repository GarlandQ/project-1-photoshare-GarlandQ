from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    AddCommentView,
)
from feed import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", PostListView.as_view(), name="index"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/comment/", AddCommentView.as_view(), name="add-comment"),
    # path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", UserPostListView.as_view(), name="user-profile"),
    path("editprofile/", views.editprofile, name="editprofile"),
]

# for testing purposes only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

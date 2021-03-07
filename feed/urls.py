from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from feed import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("editprofile/", views.editprofile, name="editprofile"),
]

# for testing purposes only
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

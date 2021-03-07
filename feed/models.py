from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    pfp = models.ImageField(default="default.jpg", upload_to="profile_pictures")

    def __str__(self):
        return f"{self.user.username} Profile"


# Users can have many posts (one to many relationship)
class Posts(models.Model):
    postImage = models.ImageField(
        upload_to=None, height_field=None, width_field=None, max_length=100
    )
    postDescription = models.TextField()
    # If user is deleted, just delete the post also
    postUser = models.ForeignKey(User, on_delete=models.CASCADE)
    postDate = models.DateTimeField(default=timezone.now)


class Comments(models.Model):
    # user's comment
    usersComment = models.TextField()
    # comment's original post. if user gets deleted, delete the comment as well.
    commentsPost = models.ForeignKey(Posts, on_delete=models.CASCADE)
    # comment's user
    commentsUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentsDate = models.DateTimeField(default=timezone.now)

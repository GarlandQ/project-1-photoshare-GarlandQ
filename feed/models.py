from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    pfp = models.ImageField(default="default.jpg", upload_to="profile_pictures")

    def __str__(self):
        return f"{self.user.username} Profile"

    # Function to adjust image for page itself
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.pfp.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pfp.path)


# Users can have many posts (one to many relationship)
class Post(models.Model):
    image = models.ImageField(
        upload_to=None, height_field=None, width_field=None, max_length=100
    )
    description = models.TextField()
    # If user is deleted, just delete the post also
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.image

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    # user's comment
    content = models.TextField(max_length=100)
    # comment's original post. if user gets deleted, delete the comment as well.
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    # comment's user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Comment {} by {}".format(self.content, self.owner)

    def get_absolute_url(Post):
        return reverse("post-detail", kwargs={"pk": Post.pk})

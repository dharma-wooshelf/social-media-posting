from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.user.username


class ContentIdea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class MediaUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    media_type = models.CharField(max_length=10, choices=[("image", "Image"), ("video", "Video")])
    created_at = models.DateTimeField(auto_now_add=True)

class SocialPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    hashtags = models.TextField(blank=True)
    media = models.ForeignKey(MediaUpload, on_delete=models.SET_NULL, null=True, blank=True)
    post_type = models.CharField(max_length=20, choices=[("image", "Image Post"), ("video", "Video Post")])
    created_at = models.DateTimeField(auto_now_add=True)

class Schedule(models.Model):
    post = models.OneToOneField(SocialPost, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    published = models.BooleanField(default=False)

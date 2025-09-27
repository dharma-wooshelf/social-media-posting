from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class ContentIdea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=[("text", "Text"), ("image", "Image"), ("video", "Video")], default="text")
    tone = models.CharField(max_length=20, choices=[("informative", "Informative"), ("funny", "Funny"), ("professional", "Professional")], default="informative")
    input_prompt = models.CharField(max_length=255, default="", blank=True)
    idea_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class MediaUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="")
    media_type = models.CharField(max_length=10, choices=[("image", "Image"), ("video", "Video")])
    created_at = models.DateTimeField(auto_now_add=True)

class TTSAudio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_idea = models.ForeignKey(ContentIdea, on_delete=models.CASCADE)
    media = models.ManyToManyField(MediaUpload)
    audio_file = models.FileField(upload_to="tts/")
    script_text = models.TextField()
    voice = models.CharField(max_length=20)
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

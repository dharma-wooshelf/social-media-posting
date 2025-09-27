from django import forms
from django.contrib.auth.models import User
from .models import ContentIdea, MediaUpload, SocialPost, Schedule

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class IdeaForm(forms.ModelForm):
    class Meta:
        model = ContentIdea
        fields = ["idea_text"]

class MediaForm(forms.ModelForm):
    class Meta:
        model = MediaUpload
        fields = ["file", "media_type"]

class PostForm(forms.ModelForm):
    class Meta:
        model = SocialPost
        fields = ["caption", "hashtags", "post_type"]


    class Meta:
        model = Schedule
        fields = ["scheduled_time"]

# Profile update form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

# Social media linking form
class SocialLinkForm(forms.Form):
    facebook = forms.URLField(required=False, label="Facebook URL")
    twitter = forms.URLField(required=False, label="Twitter URL")
    instagram = forms.URLField(required=False, label="Instagram URL")
    linkedin = forms.URLField(required=False, label="LinkedIn URL")

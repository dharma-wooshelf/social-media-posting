from django import forms
from core.models import ContentIdea, MediaUpload, SocialPost, Schedule

class ContentIdeaForm(forms.ModelForm):
	class Meta:
		model = ContentIdea
		fields = ["post_type", "tone", "input_prompt", "idea_text"]

class MediaUploadForm(forms.ModelForm):
	class Meta:
		model = MediaUpload
		fields = ["file", "media_type"]

class SocialPostForm(forms.ModelForm):
	class Meta:
		model = SocialPost
		fields = ["caption", "hashtags", "media", "post_type"]

class ScheduleForm(forms.ModelForm):
	class Meta:
		model = Schedule
		fields = ["scheduled_time"]

# Video upload form (assuming MediaUpload is used for video)
class VideoUploadForm(forms.ModelForm):
	class Meta:
		model = MediaUpload
		fields = ["file", "media_type"]

# Text to Speech form (custom, not model-based)
class TextToSpeechForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea, label="Script Text")
	voice = forms.ChoiceField(choices=[("adam", "Adam"), ("sophia", "Sophia"), ("james", "James")])

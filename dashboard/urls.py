
from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('content-generation/', views.content_generation, name='content_generation'),
    path('content-ideas/', views.content_ideas, name='content_ideas'),
    path('media-selection/', views.media_selection, name='media_selection'),
    path('text-to-speech/', views.text_to_speech, name='text_to_speech'),
    path('social-post/', views.social_post, name='social_post'),
    path('video-create/', views.video_create, name='video_create'),
    path('video-generator/', views.video_generator, name='video_generator'),
    path('schedule-publish/', views.schedule_publish, name='schedule_publish'),
    # path("", views.dashboard, name="dashboard"),
]

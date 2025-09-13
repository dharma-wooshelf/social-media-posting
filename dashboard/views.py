from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def content_generation(request):
    return render(request, 'content_generation.html')

def content_ideas(request):
    return render(request, 'content_ideas.html')

def media_selection(request):
    return render(request, 'media_selection.html')

def text_to_speech(request):
    return render(request, 'text_to_speech.html')

def social_post(request):
    return render(request, 'social_post.html')

def video_create(request):
    return render(request, 'video_create.html')

def video_generator(request):
    return render(request, 'video_generator.html')

def schedule_publish(request):
    return render(request, 'schedule_publish.html')

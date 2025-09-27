
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ContentIdeaForm, MediaUploadForm, SocialPostForm, ScheduleForm, VideoUploadForm, TextToSpeechForm
from core.models import ContentIdea, MediaUpload, SocialPost, Schedule

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def content_generation(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # AJAX: Generate sample ideas
            post_type = request.POST.get('post_type')
            tone = request.POST.get('tone')
            input_prompt = request.POST.get('input_prompt')
            # Generate sample ideas (stub)
            ideas = [
                f"Here is an informative post about {input_prompt}.",
                f"This post shares key insights on {input_prompt}.",
                f"An explanatory post on {input_prompt} that breaks down important information."
            ]
            return JsonResponse({"ideas": ideas})
        else:
            # Save idea (Save or Proceed)
            form = ContentIdeaForm(request.POST)
            if form.is_valid():
                idea = form.save(commit=False)
                idea.user = request.user
                idea.save()
                if 'proceed' in request.POST:
                    return redirect('media_selection')
                return redirect('content_generation')
    else:
        form = ContentIdeaForm()
    previous_ideas = ContentIdea.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'content_generation.html', {'form': form, 'previous_ideas': previous_ideas})

@login_required
def content_ideas(request):
    ideas = ContentIdea.objects.filter(user=request.user)
    return render(request, 'content_ideas.html', {'ideas': ideas})

@login_required
def media_selection(request):
    idea_id = request.GET.get('idea_id') or request.POST.get('idea_id')
    selected_idea = None
    if idea_id:
        try:
            selected_idea = ContentIdea.objects.get(id=idea_id, user=request.user)
        except ContentIdea.DoesNotExist:
            selected_idea = None
    media = MediaUpload.objects.filter(user=request.user)
    all_ideas = ContentIdea.objects.filter(user=request.user).order_by('-created_at')
    selected_media = []
    if request.method == "POST":
        if 'selected_media' in request.POST:
            selected_media = request.POST.getlist('selected_media')
        elif 'proceed_tts' in request.POST:
            # If no media selected, selected_media remains empty
            selected_media = []
    elif request.GET.get('media_ids'):
        selected_media = request.GET.get('media_ids').split(',')


    # Handle media deletion
    if request.method == "POST" and 'delete_media_id' in request.POST:
        delete_id = request.POST.get('delete_media_id')
        try:
            media_to_delete = MediaUpload.objects.get(id=delete_id, user=request.user)
            media_to_delete.file.delete(save=False)
            media_to_delete.delete()
        except MediaUpload.DoesNotExist:
            pass
        return redirect(request.path + f'?idea_id={idea_id}' if idea_id else '')

    if request.method == "POST" and 'proceed_tts' in request.POST:
        # Handle media selection/upload
        selected_media_ids = request.POST.getlist('selected_media')
        uploaded_media = None
        if request.FILES.get('file'):
            uploaded_media = MediaUpload.objects.create(user=request.user, file=request.FILES['file'], media_type='image')
            selected_media_ids.append(str(uploaded_media.id))
        # If no media selected, selected_media_ids may be empty
        # Redirect to text_to_speech with selected idea and media
        media_str = ','.join(selected_media_ids)
        return redirect(f"/text-to-speech/?idea_id={selected_idea.id if selected_idea else ''}&media_ids={media_str}")

    return render(request, 'media_selection.html', {
        'media': media,
        'selected_idea': selected_idea,
        'all_ideas': all_ideas,
        'selected_media': [int(mid) for mid in selected_media if mid],
    })

@login_required
def text_to_speech(request):
    idea_id = request.GET.get('idea_id') or request.POST.get('idea_id')
    media_ids = request.GET.get('media_ids', '').split(',') if request.GET.get('media_ids') else []
    selected_idea = None
    selected_media = []
    if idea_id:
        try:
            selected_idea = ContentIdea.objects.get(id=idea_id, user=request.user)
        except ContentIdea.DoesNotExist:
            selected_idea = None
    if media_ids:
        selected_media = MediaUpload.objects.filter(id__in=media_ids, user=request.user)
    all_ideas = ContentIdea.objects.filter(user=request.user).order_by('-created_at')
    all_media = MediaUpload.objects.filter(user=request.user)

    tts_audio_url = None
    if request.method == "POST":
        # Option to change idea
        if 'change_idea' in request.POST:
            new_idea_id = request.POST.get('idea_id')
            return redirect(f"/text-to-speech/?idea_id={new_idea_id}&media_ids={','.join([str(m.id) for m in selected_media])}")
        if 'change_media' in request.POST:
            new_media_ids = request.POST.getlist('media_ids')
            return redirect(f"/text-to-speech/?idea_id={idea_id}&media_ids={','.join(new_media_ids)}")
        form = TextToSpeechForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            voice = form.cleaned_data['voice']
            # Save TTS audio file
            audio_file = request.FILES.get('audio_file')
            from core.models import TTSAudio
            tts_obj = TTSAudio.objects.create(
                user=request.user,
                content_idea=selected_idea,
                script_text=text,
                voice=voice,
                audio_file=audio_file if audio_file else None
            )
            tts_obj.media.set(selected_media)
            tts_audio_url = tts_obj.audio_file.url if tts_obj.audio_file else None
            # Redirect to social_post with all selected options
            return redirect(f"/social-post/?idea_id={selected_idea.id}&media_ids={','.join([str(m.id) for m in selected_media])}&tts_id={tts_obj.id}")
    else:
        form = TextToSpeechForm(initial={'text': selected_idea.idea_text if selected_idea else ''})
    return render(request, 'text_to_speech.html', {
        'form': form,
        'audio_url': tts_audio_url,
        'selected_idea': selected_idea,
        'selected_media': selected_media,
        'all_ideas': all_ideas,
        'all_media': all_media,
    })

@login_required
def social_post(request):
    from core.models import TTSAudio
    idea_id = request.GET.get('idea_id')
    media_ids = request.GET.get('media_ids', '').split(',') if request.GET.get('media_ids') else []
    tts_id = request.GET.get('tts_id')
    selected_idea = None
    selected_media = []
    tts_audio = None
    if idea_id:
        try:
            selected_idea = ContentIdea.objects.get(id=idea_id, user=request.user)
        except ContentIdea.DoesNotExist:
            selected_idea = None
    if media_ids:
        selected_media = MediaUpload.objects.filter(id__in=media_ids, user=request.user)
    if tts_id:
        try:
            tts_audio = TTSAudio.objects.get(id=tts_id, user=request.user)
        except TTSAudio.DoesNotExist:
            tts_audio = None
    all_ideas = ContentIdea.objects.filter(user=request.user).order_by('-created_at')
    all_media = MediaUpload.objects.filter(user=request.user)
    all_tts = TTSAudio.objects.filter(user=request.user)
    if request.method == "POST":
        form = SocialPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('dashboard')
    else:
        form = SocialPostForm()
    return render(request, 'social_post.html', {
        'form': form,
        'selected_idea': selected_idea,
        'selected_media': selected_media,
        'tts_audio': tts_audio,
        'all_ideas': all_ideas,
        'all_media': all_media,
        'all_tts': all_tts,
    })

@login_required
def video_create(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.media_type = 'video'
            video.save()
            return redirect('video_generator')
    else:
        form = VideoUploadForm()
    return render(request, 'video_create.html', {'form': form})

@login_required
def video_generator(request):
    # Stub: could show generated videos
    return render(request, 'video_generator.html')

@login_required
def schedule_publish(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            return redirect('dashboard')
    else:
        form = ScheduleForm()
    return render(request, 'schedule_publish.html', {'form': form})

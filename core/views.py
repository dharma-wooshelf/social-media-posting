from .forms import ProfileUpdateForm, SocialLinkForm
from django.contrib.auth.decorators import login_required


# Profile update view (with social media fields)
@login_required
def update_profile_view(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        facebook = request.POST.get("facebook", "")
        twitter = request.POST.get("twitter", "")
        instagram = request.POST.get("instagram", "")
        linkedin = request.POST.get("linkedin", "")
        if form.is_valid():
            form.save()
            profile.facebook = facebook
            profile.twitter = twitter
            profile.instagram = instagram
            profile.linkedin = linkedin
            profile.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, "profile_update.html", {
        "form": form,
        "profile": profile,
    })

# Social media linking view
@login_required
def link_social_view(request):
    profile = request.user.profile
    if request.method == "POST":
        form = SocialLinkForm(request.POST)
        if form.is_valid():
            profile.facebook = form.cleaned_data["facebook"]
            profile.twitter = form.cleaned_data["twitter"]
            profile.instagram = form.cleaned_data["instagram"]
            profile.linkedin = form.cleaned_data["linkedin"]
            profile.save()
            return redirect("profile")
    else:
        form = SocialLinkForm(initial={
            "facebook": profile.facebook,
            "twitter": profile.twitter,
            "instagram": profile.instagram,
            "linkedin": profile.linkedin,
        })
    return render(request, "link_social.html", {"form": form})
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from .forms import SignupForm

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = True  # User created but not verified yet
            user.save()

            # Create Profile with token
            profile = Profile.objects.create(user=user)

            # Send verification email
            verify_link = f"http://127.0.0.1:8000/verify/{profile.verification_token}/"
            send_mail(
                "Verify your account",
                f"Click the link to verify your account: {verify_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            return render(request, "registration/verify_sent.html", {"email": user.email})
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

def verify_view(request, token):
    try:
        profile = Profile.objects.get(verification_token=token)
        profile.email_verified = True
        profile.save()
        return render(request, "registration/verify_success.html")
    except Profile.DoesNotExist:
        return render(request, "registration/verify_failed.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, "profile") and user.profile.email_verified:
                print(user)
                login(request, user)
                return redirect("dashboard")
            else:
                return render(request, "registration/login.html", {"error": "Email not verified"})
        else:
            return render(request, "registration/login.html", {"error": "Invalid credentials"})
    return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

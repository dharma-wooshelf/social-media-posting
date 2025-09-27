from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("verify/<uuid:token>/", views.verify_view, name="verify"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/update/", views.update_profile_view, name="profile"),
    path("profile/link-social/", views.link_social_view, name="link_social"),
    # path("", views.dashboard, name="dashboard"),
]

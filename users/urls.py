from django.urls import path

from .views import UserLoginView, UserProfileView, UserRegistrationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/<int:user_id>/", UserProfileView.as_view(), name="profile"),
]

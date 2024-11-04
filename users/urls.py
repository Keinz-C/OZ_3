# users/urls.py
from django.urls import path

from .views import (  # ActivateUserView,
    CookieTokenRefreshView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserRegistrationView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<int:user_id>/", UserProfileView.as_view(), name="profile"),
    # path("activate/<uidb64>/<token>/", ActivateUserView.as_view(), name="activate"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
]

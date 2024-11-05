from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .forms import UserRegistrationForm
from .tokens import account_activation_token

User = get_user_model()


def hello(request):
    return render(request, "hello.html")


@method_decorator(csrf_exempt, name="dispatch")
class UserRegistrationView(APIView):
    def get(self, request) -> JsonResponse:
        return render(request, "register.html")

    def post(self, request) -> JsonResponse:
        from users.serializers import UserSerializer

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"message": "User registered successfully. Please check your email to activate your account."},
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request) -> JsonResponse:
        return render(request, "login.html")

    @method_decorator(ensure_csrf_cookie)
    def post(self, request) -> JsonResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({"message": "User logged in successfully"})
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=str(refresh.access_token),
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                value=str(refresh),
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            context = {
                "name": user.name,
                "nickname": user.nickname,
                "email": user.email,
                "phone_number": user.phone_number,
            }
            return JsonResponse(context)
        return JsonResponse({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    def post(self, request) -> JsonResponse:
        response = JsonResponse({"message": "User logged out successfully"})
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        return response


class UserProfileView(APIView):
    def get(self, request, user_id: int) -> JsonResponse:
        user = get_object_or_404(User, pk=user_id)
        profile_data = {
            "email": user.email,
            "nickname": user.nickname,
            "name": user.name,
            "phone_number": user.phone_number,
            "last_login": user.last_login,
        }
        return JsonResponse(profile_data)


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        if refresh_token:
            request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200 and "access" in response.data:
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=response.data["access"],
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            del response.data["access"]
        return response

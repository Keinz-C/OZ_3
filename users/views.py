from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.core.mail import send_mail
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .forms import UserRegistrationForm
from .tokens import account_activation_token  # 이메일 인증 토큰 생성 유틸리티

User = get_user_model()


def hello(request):
    return render(request, "hello.html")


class UserRegistrationView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # 비밀번호 암호화
            user.is_active = False  # 이메일 인증 전까지 비활성화
            user.save()

            # 이메일 인증 링크 생성
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = request.build_absolute_uri(reverse("activate", kwargs={"uidb64": uid, "token": token}))

            # 이메일 전송
            mail_subject = "Activate your account"
            message = f"Hello {user.name},\n\nPlease click the link below to activate your account:\n{activation_link}"
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return JsonResponse(
                {"message": "User registered successfully. Please check your email to activate your account."},
                status=201,
            )
        return JsonResponse({"errors": form.errors}, status=400)


class UserLoginView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        # GET 요청 시 로그인 폼 데이터를 응답하거나 로그인 페이지를 반환하도록 설정합니다.
        return JsonResponse({"message": "Please use POST to login"}, status=405)

    def post(self, request: HttpRequest) -> JsonResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
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
            return response
        return JsonResponse({"error": "Invalid email or password"}, status=400)


class UserLogoutView(View):
    def post(self, request):
        response = JsonResponse({"message": "User logged out successfully"})
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        return response


class UserProfileView(View):
    def get(self, request: HttpRequest, user_id: int) -> JsonResponse:
        user = get_object_or_404(User, pk=user_id)
        profile_data = {
            "email": user.email,
            "nickname": user.nickname,
            "name": user.name,
            "phone_number": user.phone_number,
            "last_login": user.last_login,
        }
        return JsonResponse(profile_data)


# 이메일 인증을 위한 ActivateUserView 추가
class ActivateUserView(View):
    def get(self, request: HttpRequest, uidb64: str, token: str) -> JsonResponse:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return JsonResponse({"message": "Account activated successfully"}, status=200)
        return JsonResponse({"error": "Activation link is invalid"}, status=400)


# refresh token
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

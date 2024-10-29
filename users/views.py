from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from .forms import UserRegistrationForm

User = get_user_model()


class UserRegistrationView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return JsonResponse({"message": "User registered successfully"}, status=201)
        return JsonResponse({"errors": form.errors}, status=400)


class UserLoginView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "User logged in successfully"}, status=200)
        return JsonResponse({"error": "Invalid email or password"}, status=400)


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

# your_app/auth_backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            # 이메일로 사용자 검색
            user = User.objects.get(email=email)
            # 비밀번호 확인
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

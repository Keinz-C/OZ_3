# users/serializers.py
from typing import Any

from rest_framework import serializers

from .models import Users


class UserSerializer(serializers.ModelSerializer[Users]):
    password = serializers.CharField(write_only=True)  # 비밀번호는 쓰기 전용 필드로 설정

    class Meta:
        model = Users
        fields = ["id", "email", "password", "nickname", "name", "phone_number"]  # 응답할 필드들
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, Any]) -> Users:
        # 비밀번호를 암호화하여 저장
        password = validated_data.pop("password")
        user = Users(**validated_data)
        user.set_password(password)  # 비밀번호 해싱
        user.save()
        return user

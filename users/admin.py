from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Users  # 사용자 모델을 커스텀 유저로 가정합니다.


@admin.register(Users)
class CustomUserAdmin(admin.ModelAdmin):
    class CustomUserAdmin(admin.ModelAdmin):
        # 사용자 목록에 표시할 필드들 정의
        list_display = ("email", "nickname", "phone_number", "is_admin", "is_active")

        # 사용자 목록에서 검색 가능한 필드
        search_fields = ("email", "nickname", "phone_number")

        # 필터링 옵션 추가
        list_filter = ("is_admin", "is_active")

        # 필드 수정 옵션 설정 (어드민 여부 필드는 읽기 전용)
        readonly_fields = ("is_admin",)

        # 이메일을 클릭 시 상세 페이지로 이동
        list_display_links = ("email",)

        # 상세 페이지에서 필드 구성 설정
        fieldsets = (
            (_("User Info"), {"fields": ("email", "nickname", "phone_number", "is_active", "is_admin")}),
            (_("Permissions"), {"fields": ("is_staff", "is_superuser")}),
            (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
        )

        # 사용자 추가 시 필드 구성 설정
        add_fieldsets = (
            (
                _("User Info"),
                {
                    "classes": ("wide",),
                    "fields": ("email", "nickname", "phone_number", "password1", "password2", "is_active"),
                },
            ),
        )

        # 유저 목록에서 필드 정렬
        ordering = ("email",)

    # 유저 목록에서 필드 정렬
    ordering = ("email",)

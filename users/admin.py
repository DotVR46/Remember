from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "bio",
        "twitter",
        "facebook",
        "instagram",
    )


# Создаем Inline-админку для профиля пользователя
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "Профиль пользователя"
    verbose_name_plural = "Профиль пользователя"


# Расширяем стандартную админку пользователей
class UserAdmin(DefaultUserAdmin):
    inlines = [UserProfileInline]  # Включаем профиль в админку пользователя
    list_display = ("username", "is_staff", "is_active")
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "username")
    ordering = ("email",)
    fieldsets = (
        ("Основная информация", {"fields": ("email", "username", "password")}),
        ("Права доступа", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("date_joined", "last_login")}),
    )
    add_fieldsets = (
        ("Создать пользователя", {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions",
            )
        }),
    )


# Перерегистрируем модель User с новой админкой
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

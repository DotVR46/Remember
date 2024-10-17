from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
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
    verbose_name_plural = 'Профили пользователей'


# Расширяем стандартную админку пользователей
class UserAdmin(DefaultUserAdmin):
    inlines = [UserProfileInline]  # Включаем профиль в админку пользователя


# Перерегистрируем модель User с новой админкой
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

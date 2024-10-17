from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Профиль пользователя"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="Краткая биография")
    twitter = models.URLField(max_length=200, blank=True, verbose_name="Twitter")
    facebook = models.URLField(max_length=200, blank=True, verbose_name="Facebook")
    instagram = models.URLField(max_length=200, blank=True, verbose_name="Instagram")

    def __str__(self):
        return self.user.username

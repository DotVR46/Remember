# Generated by Django 5.0.7 on 2024-10-17 18:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        blank=True, max_length=500, verbose_name="Краткая биография"
                    ),
                ),
                ("twitter", models.URLField(blank=True, verbose_name="Twitter")),
                ("facebook", models.URLField(blank=True, verbose_name="Facebook")),
                ("instagram", models.URLField(blank=True, verbose_name="Instagram")),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, default="avatars/avatar.jpg", upload_to="avatars/"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
        ),
    ]

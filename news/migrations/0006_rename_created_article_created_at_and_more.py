# Generated by Django 5.0.7 on 2024-08-18 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0005_comment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="created",
            new_name="created_at",
        ),
    ]

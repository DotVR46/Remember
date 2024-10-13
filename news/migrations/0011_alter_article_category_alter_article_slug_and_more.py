# Generated by Django 5.0.7 on 2024-10-06 18:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0010_comment_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="post_category",
                to="news.category",
                verbose_name="Категория",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(max_length=300, unique=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="title",
            field=models.CharField(max_length=300, verbose_name="Заголовок"),
        ),
    ]
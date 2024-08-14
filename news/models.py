from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    # Модель новостей

    title = models.CharField(verbose_name="Заголовок", max_length=150)
    content = models.TextField(verbose_name="Текст записи")
    created = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    published = models.BooleanField(verbose_name="Статус публикации", default=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}-{self.author.username}"

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

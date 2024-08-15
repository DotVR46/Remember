from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Article(models.Model):
    # Модель новостей

    title = models.CharField(verbose_name="Заголовок", max_length=150)
    slug = models.SlugField(null=False, unique=True)
    content = models.TextField(verbose_name="Текст записи")
    created = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    published = models.BooleanField(verbose_name="Статус публикации", default=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="uploads/", default="media/stock-article.jpg", blank=True)

    def __str__(self):
        return f"{self.title}-{self.author.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

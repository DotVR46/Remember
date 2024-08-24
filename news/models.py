from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager


class Article(models.Model):
    # Модель новостей

    title = models.CharField(verbose_name="Заголовок", max_length=150)
    slug = models.SlugField(null=False, unique=True)
    content = models.TextField(verbose_name="Текст записи")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    published = models.BooleanField(verbose_name="Статус публикации", default=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    cover = models.ImageField(
        upload_to="uploads/", default="stock-article.jpg", blank=True
    )
    tags = TaggableManager()

    def __str__(self):
        return f"{self.title}-{self.author.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name="Запись",
        related_name="comments",
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    text = models.CharField(max_length=300, verbose_name="Текст")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Коммент от {self.user.username} на {self.article.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

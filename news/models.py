from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager


class Category(models.Model):
    """Категории"""

    name = models.CharField(verbose_name="Название", max_length=20)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Article(models.Model):
    """Записи"""

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
    category = models.ForeignKey(
        Category,
        verbose_name="Категории",
        on_delete=models.DO_NOTHING,
        blank=True,
        related_name="post_category",
    )

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
    """Комментарии"""

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
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"Коммент от {self.user.username} на {self.article.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

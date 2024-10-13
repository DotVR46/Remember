from django.contrib import admin, messages

from news.models import Article, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def save_model(self, request, obj, form, change):
        if Category.objects.count() >= 3 and not change:
            messages.error(request, "Вы не можете создать более трех категорий.")
            return  # Прерываем сохранение объекта
        super().save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "published", "category")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at")

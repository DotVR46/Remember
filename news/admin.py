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
    list_filter = ("category", "published")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at", "is_approved")
    list_editable = ("is_approved",)
    actions = ["approve_comments", "disapprove_comments"]

    def approve_comments(self, request, queryset):
        """Опубликовать комментарий"""
        row_update = queryset.update(is_approved=True)
        message_bit = f"Записей обновлено: {row_update}"
        self.message_user(request, message_bit)

    def disapprove_comments(self, request, queryset):
        """Снять с публикации комментарий"""
        row_update = queryset.update(is_approved=False)
        message_bit = f"Записей обновлено: {row_update}"
        self.message_user(request, message_bit)

    approve_comments.short_description = "Опубликовать комментарий"
    approve_comments.allowed_permissions = ("change",)
    disapprove_comments.short_description = "Снять с публикации комментарий"
    disapprove_comments.allowed_permissions = ("change",)

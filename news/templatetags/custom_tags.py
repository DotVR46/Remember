from django import template
from taggit.models import Tag

from news.models import Article

register = template.Library()


@register.simple_tag
def get_last_5_articles(exclude_article_id=None):
    """
    Возвращает последние 5 статей, исключая или нет указанную статью по ID
    """

    if exclude_article_id:
        queryset = Article.objects.exclude(id=exclude_article_id).order_by("-created_at")[:5]
    else:
        queryset = Article.objects.all().order_by("-created_at")[:5]
    return queryset


@register.simple_tag
def get_random_tags(count=10):
    return Tag.objects.order_by("?")[:count]

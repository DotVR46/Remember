from django import template
import random
from taggit.models import Tag

from news.models import Article

register = template.Library()


@register.filter
def comment_declension(count):
    # Выводим нужное слово в зависимости от количества комментариев

    if count % 10 == 1 and count % 100 != 11:
        return f"{count} комментарий"
    elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
        return f"{count} комментария"
    else:
        return f"{count} комментариев"


@register.filter
def random_articles(articles, count=5):
    articles_list = list(articles)
    random.shuffle(articles_list)  # Перемешиваем статьи
    return articles_list[:count]  # Возвращаем первые count (по умолчанию 5)


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

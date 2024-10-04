from django import template
import random

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

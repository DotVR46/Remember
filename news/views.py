from django.shortcuts import render
from django.views import generic
from news.models import Article


class IndexPageView(generic.ListView):
    template_name = "pages/index.html"
    context_object_name = "news_by_category"  # Имя переменной контекста в шаблоне

    def get_queryset(self):
        # Получаем все новости, отсортированные по категории и дате публикации
        all_news = Article.objects.select_related("category").order_by(
            "category", "-pub_date"
        )

        # Группируем новости по категориям и отбираем последние 10 для каждой
        categorized_news = {}
        for news in all_news:
            if news.category not in categorized_news:
                categorized_news[news.category] = []
            if len(categorized_news[news.category]) < 10:
                categorized_news[news.category].append(news)

        return categorized_news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем выборку последних 10 новостей вне зависимости от категории
        last_10_news = Article.objects.order_by("-pub_date")[:10]

        # Добавляем результаты в контекст
        context["news_by_category"] = self.get_queryset()
        context["last_10_news"] = last_10_news

        return context


class ArticleDetailView(generic.DetailView):
    model = Article
    context_object_name = "article"
    template_name = "pages/article_detail.html"

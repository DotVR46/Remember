from django.db.models import OuterRef, Subquery
from django.shortcuts import render
from django.views import generic
from news.models import Article


class IndexPageView(generic.ListView):
    template_name = "pages/index.html"
    context_object_name = "articles_by_category"  # Имя переменной контекста в шаблоне

    def get_queryset(self):
        # Подзапрос для получения последних 10 новостей в каждой категории
        subquery = (
            Article.objects.filter(category=OuterRef("category"))
            .order_by("-created_at")
            .values("id")[:10]
        )

        # Основной запрос, фильтрующий новости по результатам подзапроса
        news_by_category = Article.objects.filter(id__in=Subquery(subquery))

        # Группировка новостей по категориям
        categorized_news = {}
        for news in news_by_category:
            if news.category not in categorized_news:
                categorized_news[news.category] = []
            categorized_news[news.category].append(news)

        return categorized_news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем последние 10 новостей вне зависимости от категории
        last_10_news = Article.objects.order_by("-created_at")[:10]

        # Добавляем данные в контекст
        context["articles_by_category"] = self.get_queryset()
        context["last_10_articles"] = last_10_news

        return context


class ArticleDetailView(generic.DetailView):
    model = Article
    context_object_name = "article"
    template_name = "pages/article_detail.html"

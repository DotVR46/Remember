from django.db.models import OuterRef, Subquery, Q
from django.views import generic
from taggit.models import Tag

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
        articles_by_category = Article.objects.filter(id__in=Subquery(subquery))

        # Группировка новостей по категориям
        categorized_articles = {}
        for articles in articles_by_category:
            if articles.category not in categorized_articles:
                categorized_articles[articles.category] = []
            categorized_articles[articles.category].append(articles)

        return categorized_articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем последние 10 новостей вне зависимости от категории
        last_10_articles = Article.objects.order_by("-created_at")[:10]

        # Добавляем данные в контекст
        context["articles_by_category"] = self.get_queryset()
        context["last_10_articles"] = last_10_articles

        return context


class ArticleDetailView(generic.DetailView):
    model = Article
    context_object_name = "article"
    template_name = "pages/article_detail.html"

    def get_queryset(self):
        # Получаем slug статьи для детализированного просмотра
        article_slug = self.kwargs.get('slug')

        # Выбираем текущий пост и последние 5 постов за один запрос
        return Article.objects.filter(
            Q(slug=article_slug) | Q(id__in=Article.objects.order_by('-created_at').values('id')[:5])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Передаем 5 последних статей в контекст, исключая текущую статью
        context['last_5_articles'] = Article.objects.exclude(id=self.object.id).order_by('-created_at')[:5]

        # Собираем 10 случайных тегов
        context['tags'] = Tag.objects.order_by('?')[:10]

        return context

from django.db.models import OuterRef, Subquery, Q, Count
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from taggit.models import Tag

from news.forms import CommentForm
from news.models import Article, Category


class IndexPageView(generic.ListView):
    template_name = "pages/index.html"
    context_object_name = "articles_by_category"  # Имя переменной контекста в шаблоне

    def get_queryset(self):
        # Подзапрос для получения последних 10 новостей в каждой категории
        subquery = (
            Article.objects.filter(category=OuterRef("category"))
            .order_by("-created_at")
            .values("id")[:15]
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

    @staticmethod
    def post(request, slug):
        article = Article.objects.get(slug=slug)
        user = request.user
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.article = article
            form.user = user
            form.save()
        return redirect(article.get_absolute_url())


class ArticleListView(generic.ListView):
    model = Article
    context_object_name = "articles"
    template_name = "pages/article_list.html"
    paginate_by = 6

    def get_queryset(self):
        slug = self.kwargs["slug"]
        return Article.objects.filter(category__slug=slug).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем объект категории по slug и добавляем его в контекст
        category = get_object_or_404(Category, slug=self.kwargs["slug"])
        context["category"] = category
        return context


class SearchView(generic.ListView):
    model = Article
    context_object_name = "articles"
    template_name = "pages/article_list.html"
    paginate_by = 6
    ordering = ["-created_at"]

    def post(self, request, *args, **kwargs):
        query = request.POST.get("query")
        if query:
            self.object_list = Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).order_by("-created_at")
        else:
            self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data())


class TagListView(generic.ListView):
    model = Article
    context_object_name = "articles"
    template_name = "pages/article_list.html"
    paginate_by = 6

    def get_queryset(self):
        tag_slug = self.kwargs["tag_slug"]
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Article.objects.filter(tags=self.tag).order_by("-created_at")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


class ContactView(generic.TemplateView):
    template_name = "pages/contact.html"

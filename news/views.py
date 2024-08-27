from django.shortcuts import render
from django.views import generic
from news.models import Article


class IndexPageView(generic.ListView):
    queryset = Article.objects.all()
    context_object_name = "articles"
    template_name = "pages/index.html"


class ArticleDetailView(generic.DetailView):
    model = Article
    context_object_name = "article"
    template_name = "pages/article_detail.html"

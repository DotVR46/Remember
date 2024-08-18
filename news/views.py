from django.shortcuts import render

from news.models import Article


def index(request):
    articles = Article.objects.all()
    return render(request, "pages/index.html", {"articles": articles})

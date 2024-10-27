from django.urls import path

from news import views

urlpatterns = [
    path("", views.IndexPageView.as_view(), name="main-page"),
    path(
        "article/<str:slug>/", views.ArticleDetailView.as_view(), name="article-detail"
    ),
    path(
        "category/<str:slug>/",
        views.ArticleListView.as_view(),
        name="category-list",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]

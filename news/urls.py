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
    path("tag/<str:tag_slug>/", views.TagListView.as_view(), name="articles-by-tag"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]

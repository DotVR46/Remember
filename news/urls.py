from django.urls import path

from news.views import IndexPageView

urlpatterns = [
    path("", IndexPageView.as_view(), name="main-page"),
]

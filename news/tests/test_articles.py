from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timedelta

from news.models import Category, Article

User = get_user_model()


class IndexPageViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем категории
        cls.category1 = Category.objects.create(name="Category 1", slug="category-1")
        cls.category2 = Category.objects.create(name="Category 2", slug="category-2")
        # Создаем пользователя
        cls.user = User.objects.create_user(username="testuser", password="testpass")
        # Создаем статьи для каждой категории
        for i in range(15):
            Article.objects.create(
                title=f"Article {i + 1} in Category 1",
                content="Some content here",
                created_at=datetime.now() - timedelta(days=i),
                category=cls.category1,
                author=cls.user,
            )

            Article.objects.create(
                title=f"Article {i + 1} in Category 2",
                content="Some content here",
                created_at=datetime.now() - timedelta(days=i),
                category=cls.category2,
                author=cls.user,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("main-page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/index.html")

    def test_view_returns_last_10_articles(self):
        response = self.client.get(reverse("main-page"))
        self.assertEqual(response.status_code, 200)

        last_10_articles = Article.objects.order_by("-created_at")[:10]
        response_articles = response.context["last_10_articles"]

        self.assertEqual(len(response_articles), 10)
        self.assertQuerySetEqual(
            response_articles, last_10_articles, transform=lambda x: x
        )

    def test_view_groups_articles_by_category(self):
        response = self.client.get(reverse("main-page"))
        self.assertEqual(response.status_code, 200)

        articles_by_category = response.context["articles_by_category"]

        # Проверяем, что каждая категория содержит не более 15 статей
        self.assertIn(self.category1, articles_by_category)
        self.assertIn(self.category2, articles_by_category)
        self.assertEqual(len(articles_by_category[self.category1]), 15)
        self.assertEqual(len(articles_by_category[self.category2]), 15)

    def test_view_contains_expected_articles_for_each_category(self):
        response = self.client.get(reverse("main-page"))
        self.assertEqual(response.status_code, 200)

        articles_by_category = response.context["articles_by_category"]
        category1_articles = articles_by_category[self.category1]
        category2_articles = articles_by_category[self.category2]

        # Проверяем, что статьи правильно отсортированы в каждой категории
        self.assertEqual(
            [article.title for article in category1_articles],
            [f"Article {i + 1} in Category 1" for i in range(15)],
        )
        self.assertEqual(
            [article.title for article in category2_articles],
            [f"Article {i + 1} in Category 2" for i in range(15)],
        )

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Page
from news.models import Article, Category


class ProfileViewTestCase(TestCase):

    def setUp(self):
        # Создаем пользователя и статьи
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        # Создаем 10 статей для проверки пагинации
        for i in range(10):
            Article.objects.create(
                author=self.user,
                title=f"Article {i}",
                content="Content",
                slug=f"article-{i}",
                category=self.category
            )

    def test_profile_view_status_code(self):
        response = self.client.get(reverse("profile", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_uses_correct_template(self):
        response = self.client.get(reverse("profile", args=[self.user.id]))
        self.assertTemplateUsed(response, "pages/profile.html")

    def test_profile_view_context_contains_user(self):
        response = self.client.get(reverse("profile", args=[self.user.id]))
        self.assertEqual(response.context["user"], self.user)

    def test_profile_view_shows_user_articles(self):
        response = self.client.get(reverse("profile", args=[self.user.id]))
        articles = response.context["articles"]
        self.assertEqual(
            len(articles), 6
        )  # Пагинация должна показывать 6 статей на первой странице
        self.assertTrue(all(article.author == self.user for article in articles))

    def test_profile_view_pagination(self):
        response = self.client.get(reverse("profile", args=[self.user.id]))
        page_obj = response.context["page_obj"]
        self.assertIsInstance(page_obj, Page)
        self.assertEqual(
            page_obj.paginator.num_pages, 2
        )  # 10 статей, 6 на первой странице, 4 на второй
        self.assertEqual(page_obj.number, 1)  # Первая страница

        # Проверяем вторую страницу
        response = self.client.get(reverse("profile", args=[self.user.id]) + "?page=2")
        page_obj = response.context["page_obj"]
        self.assertEqual(page_obj.number, 2)
        self.assertEqual(
            len(page_obj.object_list), 4
        )  # На второй странице должно быть оставшиеся 4 статьи

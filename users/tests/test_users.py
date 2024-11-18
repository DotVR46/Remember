from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Page
from news.models import Article, Category


class ProfileViewTestCase(TestCase):

    def setUp(self):
        # Создаем пользователя и статьи
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        # Создаем 10 статей для проверки пагинации
        for i in range(10):
            Article.objects.create(
                author=self.user,
                title=f"Article {i}",
                content="Content",
                slug=f"article-{i}",
                category=self.category,
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


class UserRegisterViewTestCase(TestCase):

    def test_register_view_uses_correct_template(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_successful_registration_creates_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password1": "Testpassword123",
                "password2": "Testpassword123",
            },
        )
        # Проверка, что пользователь был создан
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, "testuser")
        # Проверка, что используется шаблон успешной регистрации
        self.assertTemplateUsed(response, "registration/register_done.html")

    def test_registration_password_mismatch(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password1": "Testpassword123",
                "password2": "Wrongpassword123",
            },
        )
        # Пользователь не должен быть создан
        self.assertEqual(User.objects.count(), 0)
        # Проверка, что используется шаблон для повторной попытки регистрации
        self.assertTemplateUsed(response, "registration/register.html")
        # Проверка, что форма вернулась с ошибкой
        self.assertContains(response, "Пароли не совпадают!")


class LoginViewTest(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser", password="Testpassword123"
        )

    def test_login_view_status_code(self):
        # Проверка доступности страницы логина
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_successful(self):
        # Проверка успешного входа с правильным логином и паролем
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "Testpassword123"}
        )
        # Проверка, что после успешного входа пользователь перенаправляется на страницу после входа (например, на главную)
        self.assertRedirects(
            response, reverse("main-page")
        )  # Замените на ваш путь после входа
        # Проверка, что пользователь залогинен
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):
        # Проверка, что при неверных данных вход не удастся
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "Wrongpassword123"}
        )
        # Проверка, что ошибка появилась и форма снова рендерится
        self.assertContains(
            response, "Ваши логин и пароль не совпадают, попробуйте еще раз."
        )
        # Проверка, что пользователь не залогинен
        self.assertFalse(response.wsgi_request.user.is_authenticated)

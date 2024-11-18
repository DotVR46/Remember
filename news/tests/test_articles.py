from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timedelta

from taggit.models import Tag

from news.models import Category, Article, Comment

User = get_user_model()


class IndexPageViewTestCase(TestCase):

    def setUp(self):
        # Создаем категории
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", slug="category-2")
        # Создаем пользователя
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Создаем статьи для каждой категории
        for i in range(15):
            Article.objects.create(
                title=f"Article {i + 1} in Category 1",
                content="Some content here",
                created_at=datetime.now() - timedelta(days=i),
                category=self.category1,
                author=self.user,
            )

            Article.objects.create(
                title=f"Article {i + 1} in Category 2",
                content="Some content here",
                created_at=datetime.now() - timedelta(days=i),
                category=self.category2,
                author=self.user,
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


class ArticleDetailViewTestCase(TestCase):

    def setUp(self):
        # Создаем тестового пользователя, статью и начальные комментарии
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", slug="category-2")
        self.user = User.objects.create_user(username="testuser", password="password")
        self.article = Article.objects.create(
            title="Test Article",
            category=self.category1,
            content="Test content",
            author=self.user,
        )
        self.parent_comment = Comment.objects.create(
            text="Parent comment", article=self.article, user=self.user
        )
        self.child_comment = Comment.objects.create(
            text="Child comment",
            article=self.article,
            user=self.user,
            parent=self.parent_comment,
        )
        self.article_url = reverse("article-detail", args=[self.article.slug])

    def test_article_detail_view_renders_correct_template(self):
        response = self.client.get(self.article_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/article_detail.html")

    def test_article_detail_view_contains_comments(self):
        response = self.client.get(self.article_url)
        self.assertIn(self.parent_comment, response.context["article"].comments.all())
        self.assertIn(self.child_comment, response.context["article"].comments.all())

    def test_post_comment_as_authenticated_user(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.article_url,
            {
                "text": "New comment",
                "parent": "",
                "user": self.user,  # Пустое значение для корневого комментария
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(text="New comment", article=self.article).exists()
        )

    def test_post_child_comment(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.article_url,
            {
                "text": "Reply to parent",
                "parent": self.parent_comment.id,  # Устанавливаем ID родителя для ответа
            },
        )
        self.assertEqual(response.status_code, 302)
        new_comment = Comment.objects.get(text="Reply to parent", article=self.article)
        self.assertEqual(new_comment.parent, self.parent_comment)


class ArticleListViewTestCase(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username="testuser", password="password")

        # Создаем категории
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", slug="category-2")

        # Создаем статьи
        self.article_in_category = Article.objects.create(
            title="Статья в категории",
            content="Контент статьи в категории",
            slug="test1",
            author=self.user,
            category=self.category1,
        )
        self.article_in_other_category = Article.objects.create(
            title="Статья в другой категории",
            content="Контент другой статьи в другой категории",
            slug="test2",
            author=self.user,
            category=self.category2,
        )

        # URL для списка статей в категории
        self.url = reverse("category-list", args=[self.category1.slug])

    def test_article_list_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/article_list.html")

    def test_article_list_view_filters_by_category(self):
        response = self.client.get(self.url)
        # Проверяем, что статья в данной категории присутствует в queryset
        self.assertIn(self.article_in_category, response.context["articles"])
        # Проверяем, что статья из другой категории отсутствует
        self.assertNotIn(self.article_in_other_category, response.context["articles"])

    def test_article_list_view_context_contains_category(self):
        response = self.client.get(self.url)
        # Проверяем, что объект категории присутствует в контексте
        self.assertEqual(response.context["category"], self.category1)

    def test_article_list_pagination(self):
        # Создаем дополнительные статьи для проверки пагинации
        for i in range(
                7
        ):  # Создаем всего 8 статей, чтобы активировать пагинацию при paginate_by = 6
            Article.objects.create(
                title=f"Дополнительная статья {i}",
                content=f"Контент статьи-{i}",
                author=self.user,
                category=self.category1,
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что количество статей на первой странице равно paginate_by
        self.assertEqual(len(response.context["articles"]), 6)

        # Проверяем, что вторая страница также работает корректно
        response = self.client.get(self.url + "?page=2")
        self.assertEqual(
            len(response.context["articles"]), 2
        )  # Оставшиеся 2 статьи на второй странице


class SearchViewTestCase(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        # Создаем тестовые статьи
        self.article1 = Article.objects.create(
            title="Первый тестовый заголовок",
            content="Содержание первой тестовой статьи",
            category=self.category1,
            slug="test1",
            author=self.user,
        )
        self.article2 = Article.objects.create(
            title="Второй тестовый заголовок",
            content="Содержание второй статьи, включающее слово тест",
            category=self.category1,
            slug="test2",
            author=self.user,
        )
        self.article3 = Article.objects.create(
            title="Третий заголовок",
            content="Ничего общего с словом test",
            category=self.category1,
            slug="test3",
            author=self.user,
        )

        # URL для поиска
        self.url = reverse("search")

    def test_search_view_uses_correct_template(self):
        response = self.client.post(self.url, {"query": "тест"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/article_list.html")

    def test_search_by_title_and_content(self):
        response = self.client.post(self.url, {"query": "тест"})
        # Проверяем, что статьи, содержащие "тест" в заголовке или контенте, присутствуют
        self.assertIn(self.article1, response.context["articles"])
        self.assertIn(self.article2, response.context["articles"])
        # Убеждаемся, что статья без совпадений не включена
        self.assertNotIn(self.article3, response.context["articles"])

    def test_empty_query_returns_all_articles(self):
        response = self.client.post(self.url, {"query": ""})
        # Проверяем, что возвращаются все статьи, когда нет поискового запроса
        articles = list(response.context["articles"])
        self.assertEqual(articles, list(Article.objects.order_by("-created_at")))

    def test_search_view_pagination(self):
        # Создаем дополнительные статьи для проверки пагинации
        for i in range(8):
            Article.objects.create(
                title=f"Дополнительная статья {i}",
                content="Содержание дополнительной статьи",
                author=self.user,
                category=self.category1,
                slug=f"test{i + 4}",
            )

        response = self.client.post(self.url, {"query": ""})
        self.assertEqual(response.status_code, 200)
        # Проверяем, что на первой странице paginate_by статей
        self.assertEqual(len(response.context["articles"]), 6)

        # Проверяем, что вторая страница корректно работает
        response = self.client.post(self.url + "?page=2", {"query": ""})
        self.assertEqual(
            len(response.context["articles"]), 5
        )  # Остальные статьи на второй странице


class TagListViewTestCase(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        # Создаем тестовые теги
        self.tag1 = Tag.objects.create(name="Тестовый тег 1", slug="test-tag-1")
        self.tag2 = Tag.objects.create(name="Тестовый тег 2", slug="test-tag-2")

        # Создаем тестовые статьи и назначаем им теги
        self.article1 = Article.objects.create(
            title="Статья с тегом 1",
            content="Контент статьи с тегом 1",
            author=self.user,
            category=self.category1,
            slug="test1",
        )
        self.article1.tags.add(self.tag1)

        self.article2 = Article.objects.create(
            title="Статья с тегом 2",
            content="Контент статьи с тегом 2",
            author=self.user,
            category=self.category1,
            slug="test2",
        )
        self.article2.tags.add(self.tag2)

        self.article3 = Article.objects.create(
            title="Статья с обоими тегами",
            content="Контент статьи с обоими тегами",
            author=self.user,
            category=self.category1,
            slug="test3",
        )
        self.article3.tags.add(self.tag1, self.tag2)

        # URL для просмотра тегов
        self.url = reverse("articles-by-tag", kwargs={"tag_slug": self.tag1.slug})

    def test_tag_list_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/article_list.html")

    def test_tag_filtering(self):
        response = self.client.get(self.url)
        # Проверяем, что отображаются только статьи с тегом "tag1"
        self.assertIn(self.article1, response.context["articles"])
        self.assertIn(self.article3, response.context["articles"])
        self.assertNotIn(self.article2, response.context["articles"])

    def test_context_contains_correct_tag(self):
        response = self.client.get(self.url)
        # Проверяем, что в контексте содержится нужный тег
        self.assertEqual(response.context["tag"], self.tag1)

    def test_pagination(self):
        # Создаем дополнительные статьи с тегом для проверки пагинации
        for i in range(8):
            article = Article.objects.create(
                title=f"Дополнительная статья {i}",
                content="Содержание дополнительной статьи",
                author=self.user,
                category=self.category1,
                slug=f"test{i + 4}",
            )
            article.tags.add(self.tag1)

        response = self.client.get(self.url)
        # Проверяем, что на первой странице paginate_by статей
        self.assertEqual(len(response.context["articles"]), 6)

        # Проверяем, что вторая страница корректно работает
        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(
            len(response.context["articles"]), 4
        )  # Остальные статьи на второй странице


class ContactViewTestCase(TestCase):

    def setUp(self):
        # URL для страницы контактов
        self.url = reverse("contact")

    def test_contact_view_status_code(self):
        response = self.client.get(self.url)
        # Проверяем, что ответ успешный
        self.assertEqual(response.status_code, 200)

    def test_contact_view_uses_correct_template(self):
        response = self.client.get(self.url)
        # Проверяем, что используется правильный шаблон
        self.assertTemplateUsed(response, "pages/contact.html")

    def test_contact_view_context_data(self):
        response = self.client.get(self.url)
        # Проверяем, что шаблон получил контекст, если он есть
        self.assertIn(
            "view", response.context
        )  # Django добавляет "view" в контекст по умолчанию

import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from users.models import Account

from main.models import Category, Recipe


@pytest.mark.django_db
class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.account = Account.objects.create(
            user=self.user, nickname="TestNick"
        )
        self.category = Category.objects.create(food_type="Test Category")
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            author=self.user,
        )
        self.recipe.category.add(self.category)

    def test_index_get_request(self):
        """Test GET request to index view"""
        response = self.client.get(reverse("main:main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        self.assertIn("recipes", response.context)
        self.assertIn("files", response.context)
        self.assertIn("liked", response.context)

    def test_index_post_search(self):
        """Test POST request with title search"""
        response = self.client.post(reverse("main:main"), {"title": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        self.assertIn("search_res", response.context)
        self.assertEqual(response.context["search_res"], "Test")

    def test_index_post_my_recipes_authenticated(self):
        """Test POST request for my recipes when authenticated"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("main:main"), {"my_recipes": "true"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        self.assertEqual(response.context["title"], "Мои рецепты")

    def test_index_post_my_recipes_unauthenticated(self):
        """Test POST request for my recipes when not authenticated"""
        response = self.client.post(
            reverse("main:main"), {"my_recipes": "true"}
        )
        self.assertEqual(response.status_code, 200)
        # Should still render, but without user-specific data

from django.test import TestCase
from django.contrib.auth import get_user_model

# factories
from .factories import RecipeCategoryFactory, RecipeFactory, RecipeLikeFactory
from profiles.tests.factories import UserFactory

# models
User = get_user_model()


class RecipeCategoryModelTestCase(TestCase):

    def setUp(self) -> None:
        self.recipe_category = RecipeCategoryFactory()

    def test_recipe_category_str(self):
        recipe_category = self.recipe_category
        expected_string = f'{recipe_category.id}-{recipe_category.name}'
        self.assertEqual(str(recipe_category), expected_string)


class RecipeModelTestCase(TestCase):

    def setUp(self) -> None:
        self.author = UserFactory()
        self.category = RecipeCategoryFactory()
        self.recipe = RecipeFactory(
            author=self.author, category=[self.category])

    def test_recipe_str(self):
        recipe = self.recipe
        expected_string = f'{recipe.id}-{recipe.author.username}-{recipe.title}'
        self.assertEqual(str(recipe), expected_string)

    def test_get_total_like(self):
        recipe = self.recipe
        total_like = recipe.recipelike_set.filter(
            value='Like').count()
        self.assertEqual(recipe.get_total_like, total_like)

    def test_get_total_unlike(self):
        recipe = self.recipe
        total_unlike = recipe.recipelike_set.filter(
            value='Unlike').count()
        self.assertEqual(recipe.get_total_unlike, total_unlike)


class RecipeLikeModelTestCase(TestCase):

    def setUp(self) -> None:
        self.author_recipe = UserFactory()
        self.user_like = UserFactory()
        self.recipe = RecipeFactory(author=self.author_recipe)
        self.recipe_like = RecipeLikeFactory(
            user=self.user_like, recipe=self.recipe
        )

    def test_recipe_like_str(self):
        recipe_like = self.recipe_like
        expected_string = f'{recipe_like.user.username} {recipe_like.value} {recipe_like.recipe}'
        self.assertEqual(str(recipe_like), expected_string)

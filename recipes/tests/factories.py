import factory

# models
from recipes.models import RecipeCategory, Recipe, RecipeLike

# factories
from profiles.tests.factories import ProfileFactory


class RecipeCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeCategory

    name = factory.Faker('word')


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    author = factory.SubFactory(ProfileFactory)
    category = factory.SubFactory(RecipeCategoryFactory)
    picture = factory.Faker('image_url')
    title = factory.Faker('sentence')
    descciption = factory.Faker('sentence')
    cook_time = factory.Faker('date_time')
    ingredients = factory.Faker('text')
    procedure = factory.Faker('text')


class RecipeLikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeLike

    user = factory.SubFactory(ProfileFactory)
    recipe = factory.SubFactory(RecipeFactory)
    value = factory.Faker('random_element', elements=['Like', 'Unlike'])

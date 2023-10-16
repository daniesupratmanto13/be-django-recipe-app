from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

import factory

# models
from profiles.models import Profile


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')

    profile = factory.RelatedFactory(
        'profiles.tests.factories.ProfileFactory', 'user')


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)

    @factory.post_generation
    def bookmarks(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for recipe in extracted:
                self.bookmarks.add(recipe)

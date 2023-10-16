from django.test import TestCase
from django.contrib.auth import get_user_model

# factories
from .factories import UserFactory, ProfileFactory

# Create your tests here.


class AccountUserModelTest(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_user_str(self):
        user = self.user
        expected_string = user.email
        self.assertEqual(str(user), expected_string)


class ProfileModelTest(TestCase):

    def setUp(self) -> None:
        self.profile = ProfileFactory()

    def test_profile_str(self):
        profile = self.profile
        expected_string = f'{profile.id}-{profile.user.username}'
        self.assertEqual(str(profile), expected_string)

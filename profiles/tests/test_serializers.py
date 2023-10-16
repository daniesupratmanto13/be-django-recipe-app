from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# serializers
from profiles.serializers import UserLoginSerializer

# models
User = get_user_model()


class UserSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        self.username = 'testname'
        self.email = 'test123@email.com'
        self.password = 'test@123'

    def test_create_user(self):
        url = reverse('profiles:register')
        data = {'username': self.username,
                'email': self.email,
                'password': self.password}
        response = self.client.post(url, data, format='json')
        user_created = User.objects.create_user(
            username='testname1',
            email='test1234@email.com',
            password='test@1234')
        self.assertEqual(user_created.username, 'testname1')
        self.assertEqual(user_created.email, 'test1234@email.com')
        self.assertTrue(user_created.check_password('test@1234'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

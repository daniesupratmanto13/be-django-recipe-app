from django.test import TestCase
from django.contrib.auth import get_user_model

# models
User = get_user_model()


class CustomUserManagerTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testname',
            email='test123@email.com',
            password='test@123')
        self.assertEqual(user.username, 'testname')
        self.assertEqual(user.email, 'test123@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(username='')
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="test@123")
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="test@123")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='testname',
            email='test123@email.com',
            password='test@123')
        self.assertEqual(admin_user.username, 'testname')
        self.assertEqual(admin_user.email, 'test123@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='testname', email='', password='test@123')

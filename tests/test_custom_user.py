from django.test import TestCase

from api_task.models import CustomUser, UserType


class CustomUserModelTest(TestCase):
    def setUp(self):
        # Create a user type for testing
        self.user_type, _ = UserType.objects.get_or_create(name='test_user_type')
        self.admin_type, _ = UserType.objects.get_or_create(name='admin')

    def test_create_user(self):
        # Test creating a regular user
        user = CustomUser.objects.create(username='testuser', email='test@example.com')
        default_user_type = UserType.objects.get(name="user")
        self.assertEqual(user.type, default_user_type)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        # Test creating a superuser
        superuser = CustomUser.objects.create_superuser(username='admin', email='admin@example.com')
        self.assertEqual(superuser.type, self.admin_type)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_with_type(self):
        # Test creating a user without specifying user type
        user = CustomUser.objects.create(username='testuser', email='test@example.com', type=self.user_type)
        self.assertEqual(user.type, self.user_type)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_with_type(self):
        # Test creating a superuser with a specified user type
        superuser = CustomUser.objects.create_superuser(username='admin', email='admin@example.com', type=self.admin_type)
        self.assertEqual(superuser.type, self.admin_type)
        self.assertTrue(superuser.is_superuser)

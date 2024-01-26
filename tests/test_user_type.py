from django.test import TestCase
from django.db import DataError, IntegrityError

from api_task.models import UserType


class UserTypeModelTest(TestCase):
    def setUp(self):
        # Create a UserType for testing
        self.user_type = UserType.objects.create(name='Test Type')

    def test_create_user_type(self):
        # Test creating a UserType
        self.assertEqual(UserType.objects.count(), 1)
        saved_user_type = UserType.objects.get(name='Test Type')
        self.assertEqual(saved_user_type.name, 'Test Type')

    def test_unique_user_type_name(self):
        # Test that UserType names must be unique
        with self.assertRaises(IntegrityError):
            UserType.objects.create(name='Test Type')

    def test_str_method(self):
        # Test the __str__ method of UserType
        self.assertEqual(str(self.user_type), 'Test Type')

    def test_create_user_type_without_name(self):
        # Test that creating a UserType without a name raises an error
        with self.assertRaises(IntegrityError):
            UserType.objects.create()

    def test_create_user_type_with_long_name(self):
        # Test that creating a UserType with a name longer than 50 characters raises an error
        with self.assertRaises(DataError):
            UserType.objects.create(name='a' * 51)

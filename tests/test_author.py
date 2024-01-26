from django.test import TestCase
from django.db.utils import DataError, IntegrityError

from api_task.models import Author


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='John Doe', birth_year=1903)

    def test_string_representation(self):
        self.assertEqual(str(self.author), 'John Doe (1903)')

    def test_duplicate_author(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(name="John Doe", birth_year=1903)

    def test_author_name_length(self):
        # Attempt to create an Author instance with a name longer than 100 characters
        long_name = "x" * 150

        # Use assertRaises to catch the DataError
        with self.assertRaises(DataError):
            Author.objects.create(name=long_name)

    def test_get_author(self):
        author_2 = Author.objects.create(name="John Doe", birth_year=1904)
        self.assertEqual(str(author_2), 'John Doe (1904)')
        with self.assertRaises(Author.MultipleObjectsReturned):
            Author.objects.get(name="John Doe")

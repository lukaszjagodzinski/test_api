from django.test import TestCase
from django.db.utils import IntegrityError

from api_task.models import CustomUser, Library, Book, Entry


class EntryModelTest(TestCase):
    def setUp(self):
        # Create test data
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com')
        self.library = Library.objects.create(name='Test Library')
        self.book = Book.objects.create(title='Test Book')

    def test_valid_entry_creation(self):
        # Test creating a valid entry
        entry = Entry.objects.create(user=self.user, library=self.library, book=self.book)
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.library, self.library)
        self.assertEqual(entry.book, self.book)
        self.assertIsNotNone(entry.date_added)

    def test_entry_without_user(self):
        # Test creating an entry without a user (should raise IntegrityError)
        with self.assertRaises(IntegrityError):
            Entry.objects.create(library=self.library, book=self.book)

    def test_entry_without_library(self):
        # Test creating an entry without a library (should raise IntegrityError)
        with self.assertRaises(IntegrityError):
            Entry.objects.create(user=self.user, book=self.book)

    def test_entry_without_book(self):
        # Test creating an entry without a book (should raise IntegrityError)
        with self.assertRaises(IntegrityError):
            Entry.objects.create(user=self.user, library=self.library)

    def test_entry_with_nonexistent_user(self):
        # Test creating an entry with a nonexistent user (should raise IntegrityError)
        with self.assertRaises(IntegrityError):
            Entry.objects.create(user_id=999, library=self.library, book=self.book)

    def test_entry_with_nonexistent_library(self):
        # Test creating an entry with a nonexistent library (should raise IntegrityError)
        with self.assertRaises(IntegrityError):
            Entry.objects.create(user=self.user, library_id=999, book=self.book)

    def test_entry_with_nonexistent_book(self):
        # Test creating an entry with a nonexistent book (should raise IntegrityError)
        with self.assertRaises(IntegrityError):
            Entry.objects.create(user=self.user, library=self.library, book_id=999)

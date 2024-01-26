from django.test import TestCase
from django.db.utils import DataError, IntegrityError
from api_task.models import Author, Book, BookAuthor


class BookModelTest(TestCase):
    def setUp(self):
        # Create an author for testing
        self.author = Author.objects.create(name="John Doe", birth_year=1234)

    def test_create_book(self):
        # Test creating a book with valid data
        book = Book.objects.create(title="Sample Book")
        book.authors.set([self.author])
        self.assertEqual(str(book), "Sample Book (John Doe (1234))")

    def test_unique_title_with_authors(self):
        # Test that book titles with the same authors are not allowed
        book1 = Book.objects.create(title="Unique Title")
        book1.authors.set([self.author])


        # Attempt to create another book with the same title and authors
        with self.assertRaises(IntegrityError):
            # Use the through model to create the relationship
            BookAuthor.objects.create(book=Book(title="Unique Title").save(), author=self.author)

    def test_missing_title(self):
        # Test that a book must have a title
        with self.assertRaises(IntegrityError):
            Book.objects.create()

    def test_invalid_title_length(self):
        # Test that the title length is within the specified limit
        long_title = "x" * 101
        with self.assertRaises(DataError):
            Book.objects.create(title=long_title)

    def test_add_author(self):
        # Test adding an author to a book
        book = Book.objects.create(title="Book with Author")
        book.authors.set([self.author])
        self.assertEqual(book.authors.count(), 1)

    def test_remove_author(self):
        # Test removing an author from a book
        book = Book.objects.create(title="Book without Author")
        book.authors.set([self.author])
        book.authors.remove(self.author)
        self.assertEqual(book.authors.count(), 0)

    def test_invalid_author(self):
        # Test adding an invalid author to a book (non-existent author)
        book = Book.objects.create(title="Book with Invalid Author")
        invalid_author = Author(name="Invalid Author")
        with self.assertRaises(ValueError):
            book.authors.set([invalid_author])

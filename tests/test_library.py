from django.test import TestCase

from api_task.models import Author, Book, Library


class LibraryModelTest(TestCase):
    def setUp(self):
        # Create authors
        self.author1 = Author.objects.create(name="John Doe", birth_year=1234)
        self.author2 = Author.objects.create(name="Jane Doe", birth_year=2345)
        self.author3 = Author.objects.create(name="Alice", birth_year=4321)
        self.author4 = Author.objects.create(name="Bob", birth_year=123)

        # Create books
        self.book1 = Book.objects.create(title="Sample Book")
        self.book1.authors.set([self.author1, self.author2])

        self.book2 = Book.objects.create(title="Another Book")
        self.book2.authors.set([self.author3, self.author4])

    def test_add_library(self):
        # Test adding a library with books
        library = Library.objects.create(name="City Library")
        library.books.set([self.book1, self.book2])

        self.assertEqual(library.books.count(), 2)

    def test_remove_library(self):
        # Test removing a library
        library = Library.objects.create(name="City Library")
        library.books.set([self.book1, self.book2])

        library.delete()

        with self.assertRaises(Library.DoesNotExist):
            Library.objects.get(name="City Library")

    def test_update_library(self):
        # Test updating a library's books
        library = Library.objects.create(name="City Library")
        library.books.set([self.book1])

        # Update the library with a new set of books
        new_book = Book.objects.create(title="New Book")
        new_book.authors.set([self.author1, self.author3])

        library.books.set([new_book])

        self.assertEqual(library.books.count(), 1)
        self.assertEqual(library.books.first().title, "New Book")

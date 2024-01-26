import requests
from django.core.management.base import BaseCommand

from api_task.models import Author, Book, Library


class Command(BaseCommand):
    help = "Populate database with book data from the Open Library API"

    def handle(self, *args, **options):
        # Define the Open Library API endpoint for books
        open_library_url = "https://openlibrary.org/subjects/science.json"

        try:
            # Fetch data from the Open Library API
            response = requests.get(open_library_url)
            data = response.json()

            # Extract book information from the API response
            book_data_list = data.get("works", [])

            # Loop through the book data and create objects in the database
            for book_data in book_data_list:
                title = book_data.get("title", "")
                publish_year = book_data.get("first_publish_year", None)
                authors = book_data.get("authors", [])
                subjects = book_data.get("subject", [])

                # Create or retrieve authors
                author_instances = []
                for author_data in authors:
                    author_name = author_data.get("name", "")
                    author_birth_year = author_data.get("birth_year", publish_year)

                    # Create or retrieve authors with name and birth year
                    author, created = Author.objects.get_or_create(
                        name=author_name,
                        defaults={"birth_year": author_birth_year}
                    )

                    author_instances.append(author)

                # Create or retrieve books
                book, created = Book.objects.get_or_create(title=title)
                book.authors.set(author_instances)

                # Create or retrieve library
                library_name = "Default Library"
                library, created = Library.objects.get_or_create(name=library_name)
                library.books.add(book)

            self.stdout.write(self.style.SUCCESS("Data populated successfully"))

        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f"Error fetching data from Open Library API: {e}")
            )
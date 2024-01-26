from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser, Group, Permission


class UserType(models.Model):
    """
    Custom user model extending AbstractUser.

    Attributes:
    - `email`: A unique email field for the user.
    - `type`: A foreign key to UserType, representing the user's type.

    Example:
    ```
    {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "type": {"name": "User"}
    }
    ```
    """
    name = models.CharField(max_length=50, unique=True, blank=False, default=None)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Attributes:
    - `email`: A unique email field for the user.
    - `type`: A foreign key to UserType, representing the user's type.

    Example:
    ```
    {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "type": {"name": "User"}
    }
    ```
    """
    email = models.EmailField(unique=True)
    type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """
        Override the save method to set the default user type for superusers.

        If the user is a superuser and has no specified type, set the type to 'admin'.
        For regular users, set the type to 'user'.

        Args:
        - `*args`, `**kwargs`: Additional arguments for the save method.

        Returns:
        - None
        """
        # Set the default user type to 'admin' for superusers
        if self.is_superuser and (not self.type or self.type.name == "admin"):
            admin_user_type, created = UserType.objects.get_or_create(name='admin')
            self.type = admin_user_type
        elif not self.type:
            regular_user, created = UserType.objects.get_or_create(name='user')
            self.type = regular_user

        super().save(*args, **kwargs)


class Author(models.Model):
    """
    Model representing an author.

    Attributes:
    - `name`: A character field representing the author's name.
    - `birth_year`: An additional field to ensure uniqueness in combination with the name.

    Example:
    ```
    {
        "name": "John Doe",
        "birth_year": 1980
    }
    ```
    """
    name = models.CharField(max_length=100)
    birth_year = models.PositiveIntegerField()

    class Meta:
        unique_together = ['name', 'birth_year']

    def __str__(self):
        return f"{self.name} ({self.birth_year})"


class Book(models.Model):
    """
    Model representing a book.

    Attributes:
    - `title`: A character field representing the book title.
    - `authors`: A many-to-many relationship with Author.

    Example:
    ```
    {
        "title": "Sample Book",
        "authors": [
            {"name": "John Doe"},
            {"name": "Jane Doe"}
        ]
    }
    ```
    """
    title = models.CharField(max_length=100, blank=False, default=None)
    authors = models.ManyToManyField(Author, through='BookAuthor')

    def __str__(self):
        author_names = ', '.join(str(author) for author in self.authors.all())
        return f"{self.title} ({author_names})"


class BookAuthor(models.Model):
    """
    Through model for the ManyToMany relationship between Book and Author.

    Enforces uniqueness based on the combination of Book's title and associated authors.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['book', 'author']


class Library(models.Model):
    """
    Model representing a library.

    Attributes:
    - `name`: A character field representing the library name.
    - `books`: A many-to-many relationship with Book.

    Example:
    ```
    {
        "name": "City Library",
        "books": [
            {
                "title": "Sample Book",
                "authors": [
                    {"name": "John Doe"},
                    {"name": "Jane Doe"}
                ]
            },
            {
                "title": "Another Book",
                "authors": [
                    {"name": "Alice"},
                    {"name": "Bob"}
                ]
            }
        ]
    }
    ```
    """
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class Entry(models.Model):
    """
    Model representing an entry (user interaction) with a library.

    Attributes:
    - `user`: A foreign key to the CustomUser model.
    - `library`: A foreign key to the Library model.
    - `book`: A foreign key to the Book model.
    - `date_added`: A DateTimeField representing the date the entry was added.

    Example:
    ```
    {
        "user": 1,
        "library": 1,
        "book": 1
    }
    ```
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Validate that the entry has a book, user, and library
        if not self.book_id or not Book.objects.filter(id=self.book_id).exists():
            raise IntegrityError('This entry must have a valid book.')

        if not self.user_id or not CustomUser.objects.filter(id=self.user_id).exists():
            raise IntegrityError('This entry must have a valid user.')

        if not self.library_id or not Library.objects.filter(id=self.library_id).exists():
            raise IntegrityError('This entry must belong to a valid library.')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entry by {self.user.username} for book '{self.book.title}' at {self.library.name}"

from rest_framework import serializers
from .models import UserType, CustomUser, Author, Book, BookAuthor, Library, Entry


class UserTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserType model.

    Serializes the 'name' field of UserType instances.

    Attributes:
    - `model`: The UserType model.
    - `fields`: The fields to include in the serialized representation.

    Example:
    ```
    {
        "name": "Administrator"
    }
    ```
    """
    class Meta:
        model = UserType
        fields = ["name"]


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    Serializes the 'user_type' field, which is a read-only representation of
    the user's type name.

    Attributes:
    - `model`: The CustomUser model.
    - `fields`: The fields to include in the serialized representation.

    Example:
    ```
    {
        "user_type": "Administrator"
    }
    ```
    """
    user_type = serializers.CharField(source='type.name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ["user_type"]


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Serializes the 'name' field of Author instances.

    Attributes:
    - `model`: The Author model.
    - `fields`: The fields to include in the serialized representation.

    Example:
    ```
    {
        "name": "John Doe"
    }
    ```
    """
    class Meta:
        model = Author
        fields = ["name"]


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Serializes the 'title' field and a nested representation of the 'authors'
    field using the AuthorSerializer.

    Attributes:
    - `model`: The Book model.
    - `fields`: The fields to include in the serialized representation.

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
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["title", "authors"]

    def create(self, validated_data):
        authors_data = validated_data.pop("authors")
        book = Book.objects.create(**validated_data)
        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(**author_data)
            BookAuthor.objects.create(book=book, author=author)
        return book


class LibrarySerializer(serializers.ModelSerializer):
    """
    Serializer for the Library model.

    Serializes the 'name' field and a nested representation of the 'books'
    field using the BookSerializer.

    Attributes:
    - `model`: The Library model.
    - `fields`: The fields to include in the serialized representation.

    Example:
    ```
    {
        "name": "Sample Library",
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
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Library
        fields = ["name", "books"]


class EntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the Entry model.

    Serializes the 'user' and 'library' fields of Entry instances.

    Attributes:
    - `model`: The Entry model.
    - `fields`: The fields to include in the serialized representation.

    Example:
    ```
    {
        "user": 1,
        "library": 1
    }
    ```
    """
    class Meta:
        model = Entry
        fields = ["user", "library"]

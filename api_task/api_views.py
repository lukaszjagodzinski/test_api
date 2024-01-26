from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserType, CustomUser, Author, Book, Library, Entry
from .serializers import (
    UserTypeSerializer,
    CustomUserSerializer,
    AuthorSerializer,
    BookSerializer,
    LibrarySerializer,
    EntrySerializer,
)


class UserTypeListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating UserTypes.

    This view allows clients to:
    - Retrieve a list of all existing UserTypes.
    - Create a new UserType instance by providing valid data.

    Inherits from:
    `generics.ListCreateAPIView` - Django Rest Framework class for handling
    both listing and creating objects.

    Attributes:
    - `queryset`: A queryset that retrieves all instances of the UserType model.
    - `serializer_class`: The serializer class used for serializing and
      deserializing UserType instances.

    Example:
    ```
    # To retrieve a list of UserTypes:
    GET /api/user-types/

    # To create a new UserType:
    POST /api/user-types/
    {
        "name": "New User Type"
    }
    ```

    Note: Authentication and permission classes can be added based on your
    project requirements.
    """
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer


class CustomUserListView(generics.ListAPIView):
    """
    API view for listing CustomUser instances with admin access.

    This view allows only users with admin privileges to retrieve a list of all
    CustomUser instances.

    Inherits from:
    `generics.ListAPIView` - Django Rest Framework class for handling listing
    objects.

    Attributes:
    - `queryset`: A queryset that retrieves all instances of the CustomUser model.
    - `serializer_class`: The serializer class used for serializing CustomUser instances.
    - `permission_classes`: A list of permission classes, in this case, limiting access
      to users with admin privileges (IsAdminUser).

    Example:
    ```
    # To retrieve a list of CustomUser instances (requires admin access):
    GET /api/custom-users/
    ```

    Note: Make sure to authenticate users and handle other permissions as needed
    based on your project requirements.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


class AuthorListView(generics.ListAPIView):
    """
    API view for listing Author instances.

    This view allows clients to retrieve a list of all existing Author instances.

    Inherits from:
    `generics.ListAPIView` - Django Rest Framework class for handling listing
    objects.

    Attributes:
    - `queryset`: A queryset that retrieves all instances of the Author model.
    - `serializer_class`: The serializer class used for serializing Author instances.

    Example:
    ```
    # To retrieve a list of Author instances:
    GET /api/authors/
    ```
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListView(generics.ListAPIView):
    """
    API view for listing Book instances.

    This view allows clients to retrieve a list of all existing Book instances.

    Inherits from:
    `generics.ListAPIView` - Django Rest Framework class for handling listing
    objects.

    Attributes:
    - `queryset`: A queryset that retrieves all instances of the Book model.
    - `serializer_class`: The serializer class used for serializing Book instances.

    Example:
    ```
    # To retrieve a list of Book instances:
    GET /api/books/
    ```
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class LibraryListView(generics.ListAPIView):
    """
    API view for listing Library instances.

    This view allows clients to retrieve a list of all existing Library instances.

    Inherits from:
    `generics.ListAPIView` - Django Rest Framework class for handling listing
    objects.

    Attributes:
    - `queryset`: A queryset that retrieves all instances of the Library model.
    - `serializer_class`: The serializer class used for serializing Library instances.

    Example:
    ```
    # To retrieve a list of Library instances:
    GET /api/libraries/
    ```
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class EntryCreateView(generics.CreateAPIView):
    """
    API view for creating Entry instances with admin access.

    This view allows only users with admin privileges to create new Entry instances.

    Inherits from:
    `generics.CreateAPIView` - Django Rest Framework class for handling
    creating objects.

    Attributes:
    - `queryset`: A queryset that retrieves all instances of the Entry model.
    - `serializer_class`: The serializer class used for serializing Entry instances.
    - `permission_classes`: A list of permission classes, in this case, limiting access
      to users with admin privileges (IsAdminUser).

    Example:
    ```
    # To create a new Entry (requires admin access):
    POST /api/entries/
    {
        "title": "New Entry",
        "content": "Lorem ipsum...",
        "author": 1,
        "book": 2
    }
    ```

    Note: Make sure to authenticate users and handle other permissions as needed
    based on your project requirements.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAdminUser]


class EntryUpdateView(generics.UpdateAPIView):
    """
    API view for updating an existing Entry instance.

    This view allows authenticated users to update their own Entry instances,
    while superusers can update any Entry instance.

    Inherits from:
    `generics.UpdateAPIView` - Django Rest Framework class for handling updating
    objects.

    Attributes:
    - `queryset`: A queryset that retrieves all instances of the Entry model.
    - `serializer_class`: The serializer class used for serializing Entry instances.
    - `permission_classes`: A list of permission classes, in this case, allowing
      access only to authenticated users (IsAuthenticated).

    Custom Method:
    - `perform_update`: Override this method to customize the update behavior.
      In this case, it ensures that only superusers or the owner of the Entry
      instance can perform the update.

    Example:
    ```
    # To update an existing Entry:
    PUT /api/entries/<entry_id>/
    {
        "title": "Updated Entry Title",
        "content": "Updated content..."
    }
    ```

    Note: Make sure to authenticate users and handle other permissions as needed
    based on your project requirements.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer: EntrySerializer) -> None:
        """
        Custom method to perform the update of the Entry instance.

        The method checks if the user is a superuser or the owner of the Entry
        instance before saving the updates.

        Args:
        - `serializer`: The serializer instance handling the update.

        Returns:
        - None
        """
        user = self.request.user
        if user.is_superuser or serializer.instance.user == user:
            serializer.save()

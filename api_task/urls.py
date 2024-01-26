from django.urls import path
from .api_views import (
    UserTypeListCreateView,
    CustomUserListView,
    AuthorListView,
    BookListView,
    LibraryListView,
    EntryCreateView,
    EntryUpdateView,
)


urlpatterns = [
    path("user-types/", UserTypeListCreateView.as_view(), name="user-type-list"),
    path("users/", CustomUserListView.as_view(), name="user-list"),
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("libraries/", LibraryListView.as_view(), name="library-list"),
    path("entries/create/", EntryCreateView.as_view(), name="entry-create"),
    path("entries/<int:pk>/update/", EntryUpdateView.as_view(), name="entry-update"),
]

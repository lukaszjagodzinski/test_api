from django.contrib import admin

from .models import UserType, CustomUser, Author, Book, Library, Entry

admin.site.register(UserType)
admin.site.register(CustomUser)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Entry)


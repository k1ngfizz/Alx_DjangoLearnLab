from django.contrib import admin
from django.contrib import admin
from bookshelf.models import CustomUser
from .models import Author, Book, Library, Librarian
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
#admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)

# Register your models here.

# bookshelf/forms.py

from django import forms
from .models import Book  # Assuming you have a Book model

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']  # Include fields you want to expose

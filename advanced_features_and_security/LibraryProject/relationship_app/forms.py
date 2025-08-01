from django import forms
from .models import Book  # Make sure you have a Book model

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


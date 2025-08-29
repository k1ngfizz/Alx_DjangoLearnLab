"""
Serializers for the API app.

We define:
- BookSerializer: Serializes all fields of the Book model.
- AuthorSerializer: Serializes the author name and a nested list of their books.

Custom validation is included to ensure publication_year is not in the future.
"""

from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes the Book model, including all fields.

    Adds custom validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Ensure publication_year is not in the future.
        """
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model with a nested list of their books.

    The books field uses BookSerializer to serialize related Book objects dynamically.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

"""
Relationship handling:
- The AuthorSerializer includes a 'books' field, which serializes the related Book objects for each author.
- The Book model's related_name='books' on the ForeignKey allows reverse lookup from Author to Book.
"""
"""
Defines the core data models for the API app.

We have two models:
- Author: Represents a book author.
- Book: Represents a book, linked to an Author.

The Author-Book relationship is one-to-many (an author can have many books).
"""

from django.db import models

class Author(models.Model):
    """
    Author model stores information about book authors.

    Fields:
    - name: Name of the author (string).
    """
    name = models.CharField(max_length=100, help_text="The author's full name.")

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model stores individual books.

    Fields:
    - title: Title of the book (string).
    - publication_year: Year the book was published (integer).
    - author: ForeignKey to Author, establishing a one-to-many relationship.
    """
    title = models.CharField(max_length=200, help_text="Book title.")
    publication_year = models.IntegerField(help_text="Year of publication (YYYY).")
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE,
        help_text="The author who wrote this book."
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
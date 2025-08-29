from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Author, Book

User = get_user_model()

class BookAPITestCase(APITestCase):
    """
    Comprehensive tests for Book API endpoints:
    - CRUD operations
    - Filtering, searching, ordering
    - Permissions and authentication
    """

    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='user1', password='testpass123')
        self.other_user = User.objects.create_user(username='user2', password='testpass456')

        # Create authors and books
        self.author1 = Author.objects.create(name='Author One', birth_date='1980-01-01')
        self.author2 = Author.objects.create(name='Author Two', birth_date='1975-05-10')
        self.book1 = Book.objects.create(
            title='Django for Beginners', author=self.author1, publication_year=2020
        )
        self.book2 = Book.objects.create(
            title='Advanced Python', author=self.author2, publication_year=2021
        )

        self.client = APIClient()

    # --- CRUD Tests ---

    def test_list_books(self):
        """Anyone can list books."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """Anyone can retrieve a book by ID."""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books."""
        url = reverse('book-create')
        data = {
            'title': 'Test Book',
            'author': self.author1.id,
            'publication_year': 2022
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Authenticated users can create books."""
        self.client.login(username='user1', password='testpass123')
        url = reverse('book-create')
        data = {
            'title': 'Test Book',
            'author': self.author1.id,
            'publication_year': 2022
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book_unauthenticated(self):
        """Unauthenticated users cannot update books."""
        url = reverse('book-update', args=[self.book1.id])
        data = {'title': 'Updated Title'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Authenticated users can update books."""
        self.client.login(username='user1', password='testpass123')
        url = reverse('book-update', args=[self.book1.id])
        data = {
            'title': 'Updated Title',
            'author': self.author1.id,
            'publication_year': 2020
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_book_unauthenticated(self):
        """Unauthenticated users cannot delete books."""
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        """Authenticated users can delete books."""
        self.client.login(username='user1', password='testpass123')
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # --- Filtering, Searching, and Ordering ---

    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=Django for Beginners'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')

    def test_filter_books_by_author(self):
        url = reverse('book-list') + f'?author={self.author2.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(book['author'] == self.author2.id for book in response.data))

    def test_filter_books_by_publication_year(self):
        url = reverse('book-list') + '?publication_year=2021'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(book['publication_year'] == 2021 for book in response.data))

    def test_search_books_by_title(self):
        url = reverse('book-list') + '?search=django'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Django' in book['title'] for book in response.data))

    def test_search_books_by_author_name(self):
        url = reverse('book-list') + '?search=Author Two'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(book['author'] == self.author2.id for book in response.data))

    def test_order_books_by_title(self):
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_publication_year_desc(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))


"""
Testing Guide:

- Run all tests:
    python manage.py test api

- What is tested:
    - CRUD for Book endpoints
    - Filtering, searching, ordering on Book list
    - Auth and permission requirements

- Interpreting results:
    - All tests should PASS (green).
    - FAILURES (red) indicate a bug or misconfiguration; read traceback for details.

Add more tests for edge cases or business rules as your API grows!
"""

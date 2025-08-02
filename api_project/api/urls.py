from django.urls import path
from .views import BookList

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Existing ListAPIView
    path('', include(router.urls)), 

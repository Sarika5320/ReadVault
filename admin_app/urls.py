from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('books/viewbook/<int:book_id>/', book_detail, name='book_detail'),
    path('books/', list_books, name='list_books'),
    path('books/create/', create_book, name='create_book'),
    path('books/update/<int:book_id>/', update_book, name='update_book'),
    path('books/delete/<int:book_id>/', delete_book, name='delete_book'),
    path('managebook/', manage_book, name='manage_book'),

    path('authors/', list_authors, name='list_authors'),
    path('authors/create/', create_author, name='create_author'),
    path('authors/update/<int:author_id>/', update_author, name='update_author'),
    path('authors/delete/<int:author_id>/', delete_author, name='delete_author'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
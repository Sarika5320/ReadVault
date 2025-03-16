from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from .views import home, admin_dashboard,list_books,register, user_login, user_logout,create_book, update_book, delete_book,list_authors,book_detail



urlpatterns = [
    path('', home, name='home'),
    path('adminview/', admin_dashboard, name='admin_dashboard'),

    path('books/viewbook/<int:book_id>/', book_detail, name='book_detail'),
    path('books/', list_books, name='list_books'), 
    path('books/create/', create_book, name='create_book'),
    path('books/update/<int:book_id>/', update_book, name='update_book'),
    path('books/delete/<int:book_id>/', delete_book, name='delete_book'),

    path('authors/', list_authors, name='list_authors'),
    
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#path('login/', LoginView.as_view(template_name='login.html'), name='login'),


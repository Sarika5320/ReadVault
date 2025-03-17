from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from user_app.models import Author, Book
from admin_app.forms import BookForm

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

def list_authors(request):
    authors = Author.objects.all()
    return render(request, 'list_authors.html', {'authors': authors})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book_detail.html", {"book": book})

# Create Book
@login_required
@user_passes_test(is_admin)
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render(request, "create_book.html", {"form": form})

# Update Book
@login_required
@user_passes_test(is_admin)
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "update_book.html", {"form": form})

# Delete Book
@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "delete_book.html", {"book": book})

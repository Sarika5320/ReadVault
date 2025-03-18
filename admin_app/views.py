from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from user_app.models import Author, Book
from admin_app.forms import BookForm,AuthorForm
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def list_books(request):
    books = Book.objects.all()
    
    # Choose base template based on user type
    if request.user.is_authenticated and request.user.is_staff:  # Admin users
        base_template = "admin_dashboard.html"
    else:  # Normal users
        base_template = "home-base.html"

    return render(request, 'list_books.html', {'books': books, 'base_template': base_template})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book_detail.html", {"book": book})

def manage_book(request):
    
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)

    return render(request, "managebook.html", {"books": books})


# Create Book
@login_required
@user_passes_test(is_admin)
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect("manage_book")
        else:
            messages.error(request, f"Form submission failed. Errors: {form.errors}")  # Debugging
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
            return redirect("manage_book")
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
        return redirect("manage_book")
    return render(request, "delete_book.html", {"book": book})

#MANAGE AUTHORS

# List Authors
@login_required
@user_passes_test(is_admin)
def list_authors(request):
    authors_list = Author.objects.all()
    paginator = Paginator(authors_list, 5)
    page_number = request.GET.get("page")
    authors = paginator.get_page(page_number) 
    return render(request, "list_authors.html", {"authors": authors})

# Create Author
@login_required
@user_passes_test(is_admin)
def create_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Author added successfully!")
            return redirect("list_authors")
        else:
            messages.error(request, "Form submission failed. Please check the entered data.")
    else:
        form = AuthorForm()

    return render(request, "create_author.html", {"form": form})

# Update Author
@login_required
@user_passes_test(is_admin)
def update_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, "Author updated successfully!")
            return redirect("list_authors")
        else:
            messages.error(request, "Update failed. Please check the entered data.")
    else:
        form = AuthorForm(instance=author)

    return render(request, "update_author.html", {"form": form})

# Delete Author
@login_required
@user_passes_test(is_admin)
def delete_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == "POST":
        author.delete()
        messages.success(request, "Author deleted successfully!")
        return redirect("list_authors")
    
    return render(request, "delete_author.html", {"author": author})

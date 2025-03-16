from .models import Book,Author,CarouselImage,CartItem
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm


def home(request):
    images = CarouselImage.objects.all()
    best_selling_books = Book.objects.filter(is_best_seller=True)
    context = {
        "images": images,
        "best_sellers": best_selling_books,
    }
    return render(request,'home.html',context)

def best_sellers(request):
    books = Book.objects.filter(is_best_seller=True)
    return render(request,"home.html", {"books": books})

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

# Add to cart
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # If user is not logged in, redirect to login
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to add books to your cart.")
        return redirect("login")

    # Check if the book is already in the cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if not created:
        cart_item.quantity += 1  # Increase quantity if already exists
    cart_item.save()

    messages.success(request, f"{book.title} added to cart!")
    return redirect("cart")

#view cart
def view_cart(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to view your cart.")
        return redirect("login")

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})


# User Registration View
def register(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        password = request.POST.get('password', '') 
        confirm_password = request.POST.get('confirm_password','')
        
        print(request.POST)

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")
    
    return render(request, "register.html")

# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            if user.is_superuser:
                return redirect("admin_dashboard")

            return redirect("home")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")

# User Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

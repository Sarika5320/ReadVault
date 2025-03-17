from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Book, CartItem,Payment
from admin_app.models import CarouselImage 
from user_app.forms import AuthorForm
from .models import UserProfile
import stripe
from django.conf import settings
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY



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

#Remove from cart
def remove_from_cart(request, cart_item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect("cart")


#payment gateway

def create_checkout_session(request):
    if request.method != "POST":
        return redirect("cart")  # Redirect GET requests back to cart

    if not request.user.is_authenticated:
        return redirect("login")

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if total_price == 0:
        return redirect("cart")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": int(total_price * 100),  # Convert ₹ to paise
                        "product_data": {
                            "name": "Book Purchase",
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://127.0.0.1:8000/payment-success/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:8000/payment-cancel/",
        )

        return redirect(session.url)  # Redirect the user to Stripe checkout

    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
        return redirect("cart")


#success Payment
def payment_success(request):
    session_id = request.GET.get("session_id")

    if not session_id:
        return redirect("cart")

    session = stripe.checkout.Session.retrieve(session_id)
    user = request.user
    amount_paid = session.amount_total  # Get the total amount

    if amount_paid is None:  #Handle the case where amount_total is None
        amount_paid = 0
    else:
        amount_paid = amount_paid / 100  # Convert paise to ₹

    charge_id = session.payment_intent  # Get Stripe transaction ID

    # Create Payment record
    Payment.create_payment(user, amount_paid, charge_id, success=True)

    # Clear cart after successful payment
    CartItem.objects.filter(user=user).delete()

    return render(request, "payment_success.html", {"amount": amount_paid})


#cancel payment
def payment_cancel(request):
    return render(request, "payment_cancel.html")


#user Register
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

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")
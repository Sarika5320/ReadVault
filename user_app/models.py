from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Author(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    genre = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    is_best_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart_items')  # ✅ Added related_name
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        if self.book.price is not None:
            return self.quantity * self.book.price
        return Decimal(0)  # Default to 0 if price is None

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link payment to user
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store payment amount
    stripe_charge_id = models.CharField(max_length=255, unique=True)  # Store Stripe transaction ID
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of payment
    success = models.BooleanField(default=False)  # Payment status

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - ₹{self.amount}" # type: ignore

    @classmethod
    def create_payment(cls, user, amount, charge_id, success):
        """Helper method to create a new payment record."""
        return cls.objects.create(
            user=user,
            amount=amount,
            stripe_charge_id=charge_id,
            success=success
        )


from django.db import models
from django.contrib.auth.models import User

# User Profile Model
class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.username

# Author Model
class Author(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

# Book Model
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

# Carousel Image Model
class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/', null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Carousel Image"
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link cart to user
    book = models.ForeignKey("Book", on_delete=models.CASCADE)  # Store book details
    quantity = models.PositiveIntegerField(default=1)  # Allow multiple quantities

    def total_price(self):
        return self.quantity * self.book.price  # Calculate total price

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

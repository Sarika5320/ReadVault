from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, CartItem, Book, Author,Category

admin.site.register(UserProfile)
admin.site.register(CartItem)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)

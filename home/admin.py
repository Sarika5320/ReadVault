from django.contrib import admin
from .models import UserProfile, Author, Book, CarouselImage,CartItem

admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book) 
admin.site.register(CarouselImage)
admin.site.register(CartItem)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'is_best_seller')
    list_filter = ('is_best_seller',)
try:
    admin.site.register(Book, BookAdmin)
except admin.sites.AlreadyRegistered:
    pass 
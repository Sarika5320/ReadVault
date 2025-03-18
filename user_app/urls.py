from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from .views import register, user_login, user_logout,home,view_cart,add_to_cart,remove_from_cart,create_checkout_session,payment_success,payment_cancel,search_books

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),

    path('search/', search_books, name='search_books'),

    path('cart/', view_cart, name='cart'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path("cart/remove/<int:cart_item_id>/", remove_from_cart, name="remove_from_cart"),

    path("checkout/", create_checkout_session, name="checkout"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-cancel/", payment_cancel, name="payment_cancel"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
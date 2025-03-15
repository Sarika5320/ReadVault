from django.urls import path
from .views import home, admin_dashboard

urlpatterns = [
    path('', home, name='home'),
    path('adminview/', admin_dashboard, name='admin_dashboard'),
]


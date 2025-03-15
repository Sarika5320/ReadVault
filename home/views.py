from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    return render(request, 'home.html')

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

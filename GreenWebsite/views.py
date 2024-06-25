from django.shortcuts import render
from .models import Product

def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})
# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import Product,UserProfile
from . import forms

def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})
# Create your views here.


def signup_view(request):
    form = forms.UserForm()
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('login')
    print("this should print",request.method)
    return render(request, 'registration/signup.html', {'form':form})



def login_user(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard on successful login
            else:
                # Handle invalid credentials
                form.add_error(None, 'Invalid username or password.')
    else:
        form = forms.LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('dashboard')
from django.contrib.auth.decorators import login_required
from .forms import ProductForm




@login_required
def add_product(request):
    if not request.user.userprofile.is_admin:
        return redirect('home')  # Or any other appropriate page

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not request.user.userprofile.is_admin:
        return redirect('home')  # Or any other appropriate page

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard or product list
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})
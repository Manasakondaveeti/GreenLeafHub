from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Product, UserProfile, ReviewRating
from django.contrib import messages
from . import forms
from django.contrib.auth.views import PasswordResetView
from .forms import ProductForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404

def send_test_email(request):
    send_mail(
        'Testing Email Sending',  # Subject
        'This is a test email sent from Django.',  # Message
        'greenleafhub00@example.com',  # From email address
        ['cherrydaniel11@gmail.com'],  # To email addresses (can be a list)
        fail_silently=False,  # Raise an exception if sending fails
    )
    return render(request, 'email_sent.html')

def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})


# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f'{field}: {error}')
    else:
        form = forms.UserRegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{username} logged in successfully')
                return redirect('dashboard')  # Redirect to dashboard on successful login
            else:
                # Handle invalid credentials
                form.add_error(None, 'Invalid username or password.')
                messages.warning(request, f'Invalid username or password.')
    else:
        form = forms.LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('dashboard')


class CustomPasswordResetView(PasswordResetView):
    form_class = forms.CustomPasswordResetForm
    template_name = 'registration/password_reset.html'


def product(request,pk):
    product = Product.objects.get(id=pk)
    reviews = ReviewRating.objects.filter(product=product)
    return render(request,'product.html',{'product':product,'reviews':reviews})

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = forms.ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = forms.ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

def add_cart(request,pk):
    pass


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    if request.method == 'POST':
        # Your logic for processing the form and adding a product
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, redirect to the product list page after adding the product
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_product(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        products = Product.objects.get(pk=pk)
        print(products)
        print(product)
    except Exception as e:
        print(e)
        return render(request, 'error.html', {'message': 'Product not found'})

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})
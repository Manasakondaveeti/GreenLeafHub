from django import forms
from GreenWebsite.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import ReviewRating
from .models import (Product , Subscriber)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repeat password'
        })

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address_line1', 'address_line2', 'phone_number', 'city', 'province', 'zip_code', 'country']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email or Username'  ,  'autocapitalize': 'none'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    Password = forms.PasswordInput()

class CustomPassResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password ', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'image',
            'description',
            'countInStock',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200, 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
            'countInStock': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        }

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']


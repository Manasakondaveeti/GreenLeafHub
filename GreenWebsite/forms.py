from django import forms
from GreenWebsite.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import ReviewRating
from .models import Product
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address_line1', 'address_line2', 'phone_number', 'city', 'province', 'zip_code', 'country']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    Password = forms.PasswordInput()

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
            'on_sale',
            'image_url',
            'description',
            'review_count',
            'rating',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200, 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'on_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
            'review_count': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'required': True}),
        }
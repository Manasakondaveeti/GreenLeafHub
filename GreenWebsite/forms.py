from django import forms
from GreenWebsite.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import ReviewRating
from .models import (Product , Subscriber ,Payment, ContactMessage)
from django.core.exceptions import ValidationError
import re
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_number', 'expiry_date', 'cvv', 'card_name']

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not re.match(r'^\d{16}$', card_number):
            raise ValidationError("Card number must be 16 digits.")
        return card_number

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not re.match(r'^\d{3}$', cvv):
            raise ValidationError("CVV must be 3 digits.")
        return cvv

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        try:
            expiry = datetime.strptime(expiry_date, '%m/%y')
            if expiry < datetime.now():
                raise ValidationError("The expiry date is in the past.")
        except ValueError:
            raise ValidationError("Expiry date must be in MM/YY format.")
        return expiry_date

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'city', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not forms.EmailField().clean(email):
            raise forms.ValidationError("Enter a valid email address.")
        return email


    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country.isalpha():
            raise forms.ValidationError("Enter a valid country name.")
        return country

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city.isalpha():
            raise forms.ValidationError("Enter a valid city name.")
        return city
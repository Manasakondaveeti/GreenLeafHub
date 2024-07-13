from django import forms
from GreenWebsite.models import UserProfile

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserProfile
        fields = ['email','password','confirm_password','username','first_name', 'last_name', 'address_line1', 'address_line2','phone_number', 'city', 'province', 'zip_code', 'country' ,'is_admin']
        widgets = {
            'password': forms.PasswordInput(),  # Use PasswordInput widget for password field
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please try again.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'on_sale', 'image_url', 'description', 'review_count', 'rating']

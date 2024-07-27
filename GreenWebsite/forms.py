from django import forms
from GreenWebsite.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import ReviewRating
from .models import Product, ContactMessage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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
    username = forms.CharField(label='Username', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Email or Username'  ,  'autocapitalize': 'none'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


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
            'on_sale',
            'image',
            'description',
            'review_count',
            'rating',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200, 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'on_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
            'review_count': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'required': True}),
        }

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

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

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Enter a valid phone number.")
        except phonenumbers.NumberParseException:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone_number

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
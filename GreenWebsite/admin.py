from django.contrib import admin
from .models import Product, UserProfile, ReviewRating

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(ReviewRating)
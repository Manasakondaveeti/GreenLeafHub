from django.contrib import admin
from .models import Product, UserProfile, ReviewRating , Cart , CartItem

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(ReviewRating)
admin.site.register(Cart)
admin.site.register(CartItem)
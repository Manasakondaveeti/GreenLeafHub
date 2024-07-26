from django.contrib import admin

from .models import (Product, UserProfile,SiteVisit,ReviewRating , Cart , CartItem, Order  ,OrderItem, Articles, UserSession,Subscriber )

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(ReviewRating)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Articles)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Subscriber)

admin.site.register(SiteVisit)
admin.site.register(UserSession)


from django.contrib import admin

from .models import (Product, UserProfile,
                     Subscriber,ReviewRating , Cart , CartItem, Order  ,OrderItem, Articles ,UserDailyVisit)

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(ReviewRating)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Articles)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Subscriber)

admin.site.register(UserDailyVisit)


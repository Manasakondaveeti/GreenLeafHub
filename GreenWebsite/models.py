from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    on_sale = models.BooleanField(default=False)
    image_url = models.URLField()
    description = models.TextField()
    review_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    country = models.CharField(max_length=15)
    zip_code = models.CharField(max_length=7)

    def __str__(self):
        return self.user.username

    def get_cart_count(self):
        total_quantity = \
            CartItem.objects.filter(cart__is_paid=False, cart__user=self.user).aggregate(
                total_quantity=Sum('quantity'))[
                'total_quantity']
        print("total_quantity", total_quantity)
        return total_quantity


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='my_reviews', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True, null=True)
    review = models.TextField(max_length=500, blank=True, null=True)
    rating = models.FloatField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


# article and contact-us related models
class Articles(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # one to many realtionship, one author can have many posts, one post has only one author
    def __str__(self):
        return self.title

    # alternative to the override method in ArticleCrewView
    # def get_absolute_url(self):
    #     return reverse('article-detail', kwargs={'pk':self.pk})

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

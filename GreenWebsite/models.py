from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    on_sale = models.BooleanField(default=False)
    image_url = models.URLField()
    description = models.TextField()
    review_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

class UserProfile(User):
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    country = models.CharField(max_length=15)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return self.username
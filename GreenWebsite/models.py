from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    on_sale = models.BooleanField(default=False)
    image_url = models.URLField()
    description = models.TextField()
    review_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

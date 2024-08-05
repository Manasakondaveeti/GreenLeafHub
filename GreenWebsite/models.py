from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum,Avg
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    countInStock = models.IntegerField(default=0)
    image = models.ImageField(default='default.png', blank=True, null=True, upload_to='product_img/')
    description = models.TextField()
    review_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

class SiteVisit(models.Model):
    visit_count = models.IntegerField(default=0)
    login_site_visit = models.IntegerField(default=0)

    def __str__(self):
        return f"Site Visit Count: {self.visit_count}, Login Visit Count: {self.login_site_visit}"

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.session_key}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    image = models.ImageField(default='profile_img/default.png', blank=True, null=True, upload_to='profile_img/')
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    country = models.CharField(max_length=15)
    zip_code = models.CharField(max_length=7)
    last_visit = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.image and self.image.name != 'default.png':
            self.image.delete(save=False)
        super(UserProfile, self).delete(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_cart_count(self):
        total_quantity = CartItem.objects.filter(
            cart__is_paid=False, cart__user=self.user
        ).aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_product_rating()

    def update_product_rating(self):
        product = self.product
        reviews = ReviewRating.objects.filter(product=product, status=True)
        if reviews.exists():
            average_rating = reviews.aggregate(average_rating=Avg('rating'))['average_rating']
            rounded_rating = round(average_rating * 2) / 2
            product.rating = rounded_rating
        else:
            product.rating = 0.0
        product.save()

    def __str__(self):
        return f'Review by {self.user.username}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'is_paid')
    def __str__(self):
        return self.user.username+"'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.cart.user.username+"'s product is "+ self.product.name


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


class SiteVisit(models.Model):
    visit_count = models.IntegerField(default=0)
    login_site_visit = models.IntegerField(default=0)

    def _str_(self):
        return f"Site Visit Count: {self.visit_count}, Login Visit Count: {self.login_site_visit}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Payment(models.Model):
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    card_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.card_name} - {self.card_number[-4:]}"

class BotanicalEntry(models.Model):
    botanical_name = models.CharField(max_length=100, help_text="Enter the botanical name")
    family = models.CharField(max_length=100, help_text="Enter the family name")
    origin = models.CharField(max_length=100, help_text="Enter the origin")
    chromosome_number = models.CharField(max_length=20, help_text="Enter the chromosome number")
    common_name = models.CharField(max_length=100, help_text="Enter the common name")
    soil = models.CharField(max_length=100, help_text="Enter the soil type")
    propagation = models.CharField(max_length=100, help_text="Enter the propagation method")
    seed_germination_temperature = models.CharField(max_length=50, help_text="Enter the seed germination temperature range")
    yield_info = models.CharField(max_length=100, help_text="Enter the yield information")
    varieties = models.TextField(help_text="Enter the varieties, separated by commas")
    pests_and_diseases = models.TextField(help_text="Enter the pests and diseases, separated by commas")

    def __str__(self):
        return self.botanical_name
    
class ContactMessage(models.Model):
    first_name = models.CharField(max_length=50, help_text="Enter your first name")
    last_name = models.CharField(max_length=50, help_text="Enter your last name")
    email = models.EmailField(help_text="Enter your email address")
    phone_number = models.CharField(max_length=15, help_text="Enter your phone number")
    country = models.CharField(max_length=50, help_text="Enter your country")
    city = models.CharField(max_length=50, help_text="Enter your city")
    subject = models.CharField(max_length=200, help_text="Enter the subject of your message")
    message = models.TextField(help_text="Enter your message")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.first_name} {self.last_name} - {self.subject}"
# Generated by Django 5.0.7 on 2024-07-16 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GreenWebsite', '0007_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
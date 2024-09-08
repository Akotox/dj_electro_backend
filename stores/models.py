from django.db import models
from django.contrib.auth.models import User

from address.models import Address
from orders.models import Order, OrderItem


class Store(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    coverUrl = models.URLField()
    website = models.URLField(blank=True)
    logo_url = models.URLField(blank=True)
    opening_hours = models.JSONField()  # Storing opening hours as JSON (e.g., {"mon": "9-5", "tue": "9-5"})
    store_products = models.ManyToManyField('products.Product', related_name='stores',
                                            blank=True)  # Linking products to the store
    is_featured = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)
    store_rating = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, default=3)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class StoreOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('refunded', 'Refunded'),
        ('canceled', 'Canceled'),
    ]
    store_reference = models.IntegerField(blank=True, null=True)
    order_reference = models.IntegerField(blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    order_items = models.ManyToManyField(OrderItem, related_name='store_orders', blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_reference} for Store {self.store_reference}"

from django.db import models
from address.models import Address
from products.models import Variation, Accessory, Product


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    PAYMENT_METHODS_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('balance', 'Balance'),
        ('card', 'Card'),
        ('ozow', 'Ozow'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('failed', 'Failed'),
        ('completed', 'Completed'),
        ('partial', 'Partial'),
        ('pending', 'Pending'),
    ]

    user = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS_CHOICES, default='balance')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    rated_products = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user} delivering to {self.address.address}"


class OrderItem(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    reference = models.ForeignKey('orders.Order', related_name='order_items', on_delete=models.CASCADE, null=True, blank=True)  # New reference
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=255)
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    variation_ref = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True)
    accessory_ref = models.ForeignKey(Accessory, on_delete=models.CASCADE, null=True, blank=True)
    capacity = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"OrderItem for {self.product.title} by {self.user_id} at {self.store.title}"

from django.utils import timezone
from django.db import models

from orders.models import Order
from products.models import Product
from stores.models import Store


# Create your models here.
class Rating(models.Model):
    product_rating = models.FloatField(blank=False)
    store_rating = models.FloatField(blank=False)
    review = models.CharField(max_length=256, blank=False)
    product_reference = models.ForeignKey(Product, on_delete=models.CASCADE)
    store_reference = models.ForeignKey(Store, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=256, blank=False, null=True)
    profile_image = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)
    order_reference = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating for {self.product_reference.title} by {self.user_id} at {self.store_reference.title}"

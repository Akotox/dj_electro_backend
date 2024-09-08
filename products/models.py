from django.db import models


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    imageUrl = models.URLField(blank=False)

    def __str__(self) -> str:
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=256)
    imageUrl = models.URLField(blank=False)

    def __str__(self):
        return self.title


class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('refurbished', 'Refurbished'),
        ('used', 'Used'),
    ]
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    product_type = models.CharField(max_length=100)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default=CONDITION_CHOICES[1])
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=3.0)
    rating_count = models.IntegerField(default=0)
    reviews = models.JSONField(blank=True)
    color = models.CharField(max_length=255)  # Storing list of colors
    image_urls = models.JSONField()  # Storing list of image URLs
    capacity = models.CharField(max_length=255)  # Storing list of sizes
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    store_ref = models.ForeignKey('stores.Store', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Accessory(models.Model):
    title = models.CharField(max_length=255)
    reference = models.ForeignKey('Product', related_name='accessories',
                                  on_delete=models.CASCADE)  # Link to one product
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()

    def __str__(self):
        return self.title


class Variation(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('refurbished', 'Refurbished'),
        ('used', 'Used'),
    ]
    color = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    reference = models.ForeignKey('Product', related_name='variations', on_delete=models.CASCADE)  # Link to one product
    capacity = models.CharField(max_length=50)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default=CONDITION_CHOICES[1])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.title} ({self.color}, {self.capacity})"

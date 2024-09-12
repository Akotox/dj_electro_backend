from django.db import models
from django.utils import timezone


class Address(models.Model):
    TAG_CHOICES = [
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    ]

    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    user = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    tag = models.CharField(max_length=50, choices=TAG_CHOICES, default='Home')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.contact_name} - {self.address}, {self.city}"

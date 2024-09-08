from django.contrib import admin
from products import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Brand)
admin.site.register(models.Accessory)
admin.site.register(models.Variation)
admin.site.register(models.Product)

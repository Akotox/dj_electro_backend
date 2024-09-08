from django.contrib import admin
from stores import models

# Register your models here.

admin.site.register(models.Store)
admin.site.register(models.StoreOrder)

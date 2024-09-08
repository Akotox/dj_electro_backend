
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),  # If using token authentication
    path('admin/', admin.site.urls),

    path('api/products/', include('products.urls')),
    path('api/stores/', include('stores.urls')),

    path('api/orders/', include('orders.urls')),
    path('api/ratings/', include('ratings.urls')),

    path('api/address/', include('address.urls')),
]

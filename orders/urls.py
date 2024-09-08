from django.urls import path
from . import views

urlpatterns = [
    path('user-orders/', views.OrderListView.as_view(), name='get_orders'),

    path('order/', views.OrderDetailView.as_view(), name='get_order'),

    path('add-order', views.OrderCreateView.as_view(), name='add_order'),
]
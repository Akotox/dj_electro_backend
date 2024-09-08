from django.urls import path
from . import views

urlpatterns = [
    path('reviews/user/', views.UserReviewsList.as_view(), name='get-user-reviews'),
    path('reviews/store/', views.StoreReviewsList.as_view(), name='get-store-reviews'),
    path('reviews/product/', views.ProductReviewsList.as_view(), name='get-product-reviews'),
    path('ratings/', views.AddRatingView.as_view(), name='add-rating'),
]
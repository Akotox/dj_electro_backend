from django.urls import path

from products import views

urlpatterns = [
    path('categories/home',  views.HomeCategoryList.as_view(), name='home_categories'),
    path('categories',  views.CategoryList.as_view(),  name='categories'),
    path('brands/',  views.BrandList.as_view(), name='brands'),
    path('recommendations',  views.ProductList.as_view(), name='recommendations'),
    path('discounts',  views.DiscountedProductList.as_view(), name='discounts'),
    path('category-products-list',  views.CategoryProductList.as_view(),name='category-products-list'),
    path('brand-products-list',  views.BrandProductList.as_view(), name='brand-products-list'),
    path('similar-products',  views.FilterSimilarProducts.as_view(), name='similar-products'),
    path('search',  views.ProductSearchView.as_view(), name='search'),
    path('singles',  views.GetProductById.as_view(), name='singles'),
    path('add-variations',  views.AddVariationToProduct.as_view(), name='add-variations'),
    path('add-accessory',  views.AddAccessoryToProduct.as_view(), name='add-accessory'),
    path('add-product',  views.AddProduct.as_view(), name='add-product'),
    path('check-availability',  views.CheckProductAvailability.as_view(), name='check-availability'),


]

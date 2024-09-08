from django.urls import path

from . import views

urlpatterns = [
    path('add-store',  views.CreateStoreView.as_view(), name='create_store'),
    path('retrieve',  views.GetStoresByOwnerView.as_view(), name='retrieve_store'),
    path('all-stores',  views.GetStores.as_view(), name='all_stores'),

    path('store-orders',  views.StoreOrdersListView.as_view(), name='store_orders'),

    path('store-statistics',  views.StoreOrderStatisticsView.as_view(), name='store_statistics'),

    path('sales-chart',  views.SalesChartDataView.as_view(), name='sales_chart'),

]

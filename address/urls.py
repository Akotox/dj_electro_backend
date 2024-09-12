from django.urls import path

from . import views

urlpatterns = [
    path('add-address', views.AddAddressView.as_view(), name='add_address'),
    path('retrieve', views.UserAddressesView.as_view(), name='retrieve_address'),
    path('update-address', views.UpdateDefaultAddressView.as_view(), name='update_address'),
    path('delete-address', views.DeleteAddressView.as_view(), name='delete_address'),
    path('get-address', views.GetDafaultAddressView.as_view(), name='get_address'),

]

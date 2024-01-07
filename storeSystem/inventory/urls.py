from django.urls import path
from .views import master, purchase, add_masterProduct, add_purchase, deleteMasterProduct, sales, add_sales, stock
urlpatterns = [
    path('master', master, name='master'),
    path('delete_product<int:pk>', deleteMasterProduct.as_view(), name='delete_product'),
    path('purchase', purchase, name='purchase'),
    path('sales', sales, name='sales'),
    path('stock', stock, name='stock'),
    path('add_sales', add_sales, name='add_sales'),
    path('add_masterProduct', add_masterProduct, name='add_masterProduct'),
    path('add_purchase', add_purchase, name='add_purchase'),
]
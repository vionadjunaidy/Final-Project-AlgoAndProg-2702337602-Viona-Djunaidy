from django.contrib import admin
from .models import masterProduct, Purchase, Sales, Stock

#Allow the models to be created, updated, and deleted through the Django admin page. 
admin.site.register(masterProduct)
admin.site.register(Purchase)
admin.site.register(Sales)
admin.site.register(Stock)

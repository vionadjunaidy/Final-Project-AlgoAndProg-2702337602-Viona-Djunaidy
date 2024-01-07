from django.forms import ModelForm
from .models import masterProduct, Purchase, Sales

class addMasterProduct(ModelForm):
    class Meta:
        model = masterProduct
        fields = ['product_name', 'selling_price']

class addPurchase(ModelForm):
    class Meta:
        model = Purchase
        fields = ['product_id', 'quantity', 'cost_per_product']
        labels = {
            'product_id': 'Product Name'
        }

class addSales(ModelForm):
    class Meta:
        model = Sales
        fields = ['product_id', 'quantity']
        labels = {
            'product_id': 'Product Name'
        }
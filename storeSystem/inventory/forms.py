from django.forms import ModelForm
from .models import masterProduct, Purchase, Sales

#Form to add new product to the masterProduct database. 
class addMasterProduct(ModelForm):
    class Meta:
        #Define the model used in the form. 
        model = masterProduct
        #Define the fields used in the form. 
        fields = ['product_name', 'selling_price']

#Form to add new purchase transaction to the Purchase database. 
class addPurchase(ModelForm):
    class Meta:
        #Define the model used in the form.
        model = Purchase
        #Define the fields used in the form.
        fields = ['product_id', 'quantity', 'cost_per_product']
        #Customize the label for 'product_id' field. 
        labels = {
            'product_id': 'Product Name'
        }

#Form to add new sales transaction to the Sales database. 
class addSales(ModelForm):
    class Meta:
        #Define the model used in the form.
        model = Sales
        #Define the fields used in the form.
        fields = ['product_id', 'quantity']
        #Customize the label for 'product_id' field.
        labels = {
            'product_id': 'Product Name'
        }

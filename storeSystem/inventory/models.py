from django.db import models
from django.utils import timezone

#Defining database schema.
#Represents information about a product in the master product list.
class masterProduct(models.Model):
    #A unique identifier for the product.
    product_id = models.IntegerField(primary_key=True)
    #The name of the product, limited to 10 characters.
    product_name = models.CharField(max_length=10, null=False, blank=False)
    #The selling price of the product, with a default value of 0.
    selling_price = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        # Representation the product as its name.
        return self.product_name

# Represents information about a purchase of a product.
class Purchase(models.Model):
    #A unique identifier for the product purchased, which will be inputted in the stock.
    purchase_id = models.IntegerField(primary_key=True)
    #The product that is purchased (foreign key to masterProduct).
    product_id = models.ForeignKey(masterProduct, on_delete=models.CASCADE)
    #The quantity of the product purchased.
    quantity = models.IntegerField(null=False, blank=False)
    #The cost per unit of the product, with a default value of 0.
    cost_per_product = models.IntegerField(null=False, blank=False, default=0)
    #The date when the purchase was made.
    date_of_purchase = models.DateField(default = timezone.now)

#Represents information about a sales transaction.
class Sales(models.Model):
    #A unique identifier for the sales transaction.
    sales_id = models.IntegerField(primary_key=True)
    #The product that was sold (foreign key to masterProduct).
    product_id = models.ForeignKey(masterProduct, on_delete=models.CASCADE)
    #The quantity of the product sold.
    quantity = models.IntegerField(null=False, blank=False)
    # The total value of the sales transaction (revenue).
    value_sales = models.IntegerField(null=False, blank=False, default=0)
    #The profit generated from the sales transaction.
    profit = models.IntegerField(null=False, blank=False, default=0)
    #The date when the sales transaction occurred.
    date_of_sales = models.DateField(default=timezone.now)

#Represents the stock of the products.
class Stock(models.Model):
    #A unique identifier for the stock entry.
    id = models.BigAutoField(primary_key=True)
    #The product in stock (foreign key to masterProduct).
    product_id = models.ForeignKey(masterProduct, on_delete=models.CASCADE)
    #The quantity of the product in stock.  
    quantity = models.IntegerField(null=False, blank=False)
    #The value of the stock.
    stock_value = models.IntegerField(null=True, blank=True)
from django.shortcuts import render, redirect
from .models import masterProduct, Purchase, Sales, Stock
from .forms import addMasterProduct, addPurchase, addSales
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

#Displaying the master product list.
@login_required
def master(request):
    master_products = masterProduct.objects.all()
    context = {
        "title" : "Master Product",
        "masterProducts" : master_products
    }
    return render(request, "inventory/masterProduct.html", context=context)

#Adding a new product to the master product list.
def add_masterProduct(request):
    error_message = ""
    if request.method == 'POST':
        add_form = addMasterProduct(data=request.POST)
        if add_form.is_valid():
            product_name = add_form.cleaned_data['product_name']

            #Check if a product with the same product name already exsists. 
            if masterProduct.objects.filter(product_name=product_name).exists():
                error_message = "Product with the same name already exists!"
            else:
                #Generate a new product_id based on the last record in the masterProduct table.
                last_record = masterProduct.objects.last()
                if last_record is not None:
                    last_product_id = last_record.product_id
                else:
                    last_product_id = 0
                
                product_id = last_product_id + 1
                product_name = add_form.cleaned_data['product_name']
                selling_price = add_form.cleaned_data['selling_price']

                #Create a new masterProduct instance and save it.
                new_product = masterProduct(product_id=product_id, product_name=product_name, selling_price=selling_price)
                new_product.save()
                
                #Create default values of quantity and stock value in the Stock database.
                new_stock = Stock(
                    product_id = new_product,
                    quantity = 0,
                    stock_value = 0
                )

                new_stock.save()

                return redirect("master")
        else:
            # Set the error message if the form is not valid
            error_message = "Form is not valid"
    else:
        add_form = addMasterProduct()
    
    return render(request, 'inventory/add_masterProduct.html', {"form": add_form, "error_message": error_message})

#Displaying the list of purchase transactions.
@login_required
def purchase(request):
    stock_products = Purchase.objects.all()
    context = {
        "title" : "Purchase",
        "purchases" : stock_products
    }
    return render(request, "inventory/purchase.html", context=context)

#Adding a new purchase transaction.
def add_purchase(request):
    if request.method == 'POST':
        add_purchaseForm = addPurchase(data=request.POST)
        if add_purchaseForm.is_valid():
            #Generate a new purchase_id based on the last record in the Purchase table.
            last_record = Purchase.objects.last()
            if last_record is not None:
                last_purchase_id = last_record.purchase_id
            else:
                last_purchase_id = 0
            
            purchase_id = last_purchase_id + 1
            product_id = add_purchaseForm.cleaned_data['product_id']
            quantity = add_purchaseForm.cleaned_data['quantity']
            cost_per_product = add_purchaseForm.cleaned_data['cost_per_product']

            #Create a new Purchase instance and save it.
            purchase = Purchase(purchase_id=purchase_id, product_id=product_id, quantity=quantity, cost_per_product=cost_per_product)
            purchase.save()

            try:
                #Update the stock based on the purchase quantity and cost of Purchase.
                stock_item = Stock.objects.get(product_id = product_id)
                old_stock = stock_item.quantity
                #Increment stock based on the purchase quantity.
                stock_item.quantity += quantity
                if stock_item.quantity is None:
                    stock_item.quantity = 0
                else:
                    stock_item.stock_value = (old_stock * stock_item.stock_value + quantity * cost_per_product) / (old_stock + quantity)
                stock_item.save()
            except Stock.DoesNotExist:
                #Case where the product is not in stock.
                stock_item = Stock(product_id=product_id, quantity=quantity)
                stock_item.save()

            return redirect('purchase')
    else:
        add_purchaseForm = addPurchase()
    
    return render(request, 'inventory/add_purchase.html', {"form": add_purchaseForm})

#View for displaying the list of sales transactions.
@login_required
def sales(request):
    sales = Sales.objects.all()
    total_profit = sum(s.profit for s in sales)
    context = {
        "title" : "Sales",
        "product_sales" : sales,
        "total_profit" : total_profit,
    }
    return render(request, "inventory/sales.html", context=context)

#View for adding a new sales transaction.
def add_sales(request):
    error_message = ""

    if request.method == 'POST':
        add_salesForm = addSales(data=request.POST)
        if add_salesForm.is_valid():
            #Generate a new sales_id based on the last record in the Sales table.
            last_record = Sales.objects.last()
            if last_record is not None:
                last_sales_id = last_record.sales_id
            else:
                last_sales_id = 0
            
            sales_id = last_sales_id + 1
            product_id = add_salesForm.cleaned_data['product_id']
            quantity = add_salesForm.cleaned_data['quantity']

            sales = Sales(sales_id=sales_id, product_id=product_id, quantity=quantity)

            available_stock = Stock.objects.get(product_id=product_id)
            if available_stock.quantity >= quantity:
                pricelist = masterProduct.objects.get(product_name = product_id)
                #Calculate value_sales (revenue).
                sales.value_sales = pricelist.selling_price * sales.quantity
                #Calculate profit.
                sales.profit = sales.value_sales - (available_stock.stock_value * sales.quantity)
                sales.save()
                try:
                    stock_item = Stock.objects.get(product_id = product_id)
                    #Decrement stock based on the sales quantity.
                    stock_item.quantity -= quantity
                    stock_item.save()
                
                    return redirect('sales')
                
                except Stock.DoesNotExist:
                #Case where the product is not in stock
                    pass

            else:
                    error_message = "Not enough stock available."
    else:
        add_salesForm = addSales()
    
    return render(request, 'inventory/add_sales.html', {"form": add_salesForm, "error_message": error_message})

#View for displaying the stock information.
@login_required
def stock(request):
    stocks = Stock.objects.all()    
    context = {
        "title": "Stock",
        "stocks": stocks,
    }
    return render(request, "inventory/stock.html", context=context)

#View for deleting a product from the master product list.
class deleteMasterProduct(DeleteView):
    model = masterProduct
    success_url = reverse_lazy('master')
    template_name = 'inventory/delete_product.html'
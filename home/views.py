# views.py
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Product

def create_product(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name')
        price = request.POST.get('price')
        product_id = request.POST.get('product_id')

        if action == 'add':
            try:
                # Create a new product
                Product.objects.create(name=name, price=price)
            except IntegrityError as e:
                if "decimal places" in str(e):
                    error_message = "Failed to save product. Price has too many decimal places."
                else:
                    error_message = "Failed to save product. " + str(e)
                return render(request, 'create_product.html', {'error': error_message})
            except Exception as e:
                return render(request, 'create_product.html', {'error': 'An unexpected error occurred. ' + str(e)})

            return redirect('create_product')  # Redirect to the same page

        elif action == 'delete':
            try:
                Product.objects.filter(id=product_id).delete()
            except Exception as e:
                return render(request, 'create_product.html', {'error': 'An unexpected error occurred. ' + str(e)})

            return redirect('create_product')  # Redirect to the same page


    # Handle GET request (show the form and list of products)
    products = Product.objects.all()
    return render(request, 'create_product.html', {'products': products})

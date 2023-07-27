from django.shortcuts import render
from .models import Product, ProductCategory


def all_products(request):
    products = Product.objects.all()
    product_categories = ProductCategory

    context = {
        'products': products,
        'product_categories': product_categories
    }

    return render(request, 'products/products.html', context)

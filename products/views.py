from django.shortcuts import render, get_object_or_404
from .models import Product, AdditionalImages


def all_products(request):
    """ A view to render all products """
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to render individual product details """
    product = get_object_or_404(Product, pk=product_id)
    additional_images = product.additionalimages_set.all()

    context = {
        'product': product,
        'additional_images': additional_images,
    }

    return render(request, 'products/product_detail.html', context)

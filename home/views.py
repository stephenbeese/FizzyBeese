from django.shortcuts import render
from products.views import Product, ProductCategory, FragranceCategory


def index(request):
    """ A view to return the index page """
    featured_products = Product.objects.filter(is_featured=True)
    latest_products = Product.objects.order_by('-uploaded_on')[:10]
    clearance_products = Product.objects.filter(is_clearance=True)
    sale_products = Product.objects.filter(sale_price=True)

    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'clearance_products': clearance_products,
        'sale_products': sale_products,
    }
    return render(request, 'home/index.html', context)

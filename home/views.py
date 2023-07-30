from django.shortcuts import render
from products.views import Product, ProductCategory, FragranceCategory


def index(request):
    """ A view to return the index page """
    featured_products = Product.objects.filter(is_featured=True)
    latest_products = Product.objects.order_by('-uploaded_on')[:10]

    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
    }
    return render(request, 'home/index.html', context)

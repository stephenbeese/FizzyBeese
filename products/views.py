from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, ProductCategory, FragranceCategory


def all_products(request):
    """ A view to render all products """
    products = Product.objects.all()
    query = None
    product_categories = None
    fragrance_categories = None

    if request.GET:
        if 'product_categories' in request.GET:
            categories = request.GET.getlist('product_categories')
            products = products.filter(product_categories__name__in=categories)
            categories = ProductCategory.objects.filter(name__in=categories)

        if 'fragrance_categories' in request.GET:
            categories = request.GET.getlist('fragrance_categories')
            products = products.filter(fragrance_categories__name__in=categories)
            categories = FragranceCategory.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You haven't entered any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_product_categories': product_categories,
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

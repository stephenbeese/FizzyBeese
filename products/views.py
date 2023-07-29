from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, ProductCategory, FragranceCategory


def all_products(request):
    """ A view to render all products """
    products = Product.objects.all()
    query = None
    product_category = None
    fragrance_category = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            elif sortkey == 'product_category':
                sortkey = 'product_categories__name'
            elif sortkey == 'fragrance_category':
                sortkey = 'fragrance_categories__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'product_categories' in request.GET:
            product_category = request.GET.getlist('product_categories')
            products = products.filter(product_categories__name__in=product_category)
            product_category = ProductCategory.objects.filter(name__in=product_category)

        if 'fragrance_categories' in request.GET:
            fragrance_category = request.GET.getlist('fragrance_categories')
            products = products.filter(fragrance_categories__name__in=fragrance_category)
            fragrance_category = FragranceCategory.objects.filter(name__in=fragrance_category)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You haven't entered any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_product_categories': product_category,
        'current_fragrance_categories': fragrance_category,
        'current_sorting': current_sorting,
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

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, ProductCategory, FragranceCategory, AdditionalImages
from .forms import ProductForm, AdditionalImagesForm


def all_products(request):
    """ A view to render all products """
    products = Product.objects.all().distinct()
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
            elif sortkey == 'product_categories':
                sortkey = 'product_categories__name'
            elif sortkey == 'fragrance_categories':
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

        if 'sale' in request.GET:
            products = Product.objects.filter(sale_price__isnull=False)

        if 'is_clearance' in request.GET:
            products = products.filter(is_clearance=True)

        if 'stock_remaining' in request.GET:
            products = products.order_by('stock_remaining')

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You haven't entered any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            category_queries = Q(product_categories__friendly_name__icontains=query) | Q(fragrance_categories__friendly_name__icontains=query)
            queries = queries | category_queries
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


def hidden_products(request):
    """
    Allows the admin to view all hidden products
    and change the hidden status without the use
    of the admin pannel
    """
    products = Product.objects.filter(is_hidden=True)
    template = 'products/hidden_products.html'
    context = {
        'products': products,
    }
    return render(request, template, context)


def product_detail(request, product_id):
    """ A view to render individual product details """
    product = get_object_or_404(Product, pk=product_id)
    additional_images = product.additionalimages_set.all()

    context = {
        'product': product,
        'additional_images': additional_images,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))

        else:
            messages.error(request, 'Failed to update please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are currently editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def add_image(request, product_id):
    """ Add additional images for specific products """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    additional_images = product.additionalimages_set.all()
    if request.method == 'POST':
        form = AdditionalImagesForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.product_id = product
            image_instance.save()
            messages.success(request, 'Successfully added more images')
            return redirect(reverse('product_detail', args=[product.id]))
        else: 
            messages.error(request, 'Failed to add additional images please ensure the form is valid.')
    else:
        form = AdditionalImagesForm()

    template = 'products/add_image.html'
    context = {
        'form': form,
        'product': product,
        'additional_images': additional_images,
    }
    return render(request, template, context)


@login_required
def delete_additional_image(request, image_id):
    """ View to delete additional images"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    image = get_object_or_404(AdditionalImages, pk=image_id)
    product_id = image.product_id.id
    image.delete()
    messages.success(request, 'Additional Image deleted!')
    return redirect('product_detail', product_id=product_id)

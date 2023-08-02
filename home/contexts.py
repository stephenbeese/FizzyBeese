from products.models import Product


def offers(model):
    clearance_products = Product.objects.filter(is_clearance=True)
    sale_products = Product.objects.filter(sale_price=True)

    context = {
        'clearance_products': clearance_products,
        'sale_products': sale_products,
    }

    return context

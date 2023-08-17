from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ A view to return the shopping bag page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add quantity of the specified product to the bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    # redirect_url = request.POST.get('redirect_url')

    # Redirects to the previous page with filter criteria
    redirect_url = request.META.get('HTTP_REFERER', '/')

    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        new_quantity = bag[item_id] + quantity
    else:
        new_quantity = quantity

    if new_quantity <= product.stock_remaining:
        bag[item_id] = new_quantity
        messages.success(request, f'Added {product.name} to your bag!')
    else:
        messages.error(
            request,
            f'Sorry, there is not enough stock for {product.name}. \
              You can only add up to {product.stock_remaining} items.'
            )

    request.session['bag'] = bag
    print(redirect_url)
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust quantity of the specified product in the bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > product.stock_remaining:
        messages.error(
            request,
            f'Sorry, there is not enough stock for {product.name}. \
            You can only add up to {product.stock_remaining} items. \
            Please review your shopping bag.')
    elif quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request, f'Updated {product.name} quantity to {bag[item_id]}'
            )
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag!')

    request.session['bag'] = bag
    return redirect(reverse('bag'))


def remove_from_bag(request, item_id):
    """ remove specified product from the bag """
    product = get_object_or_404(Product, pk=item_id)
    try:
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag!')
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item {e} from bag')
        return HttpResponse(status=500)

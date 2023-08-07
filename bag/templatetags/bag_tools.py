from django import template

register = template.Library()


@register.filter(name='calculate_subtotal')
def calculate_subtotal(price, quantity):
    """ function to calculate a products subtotal in the bag """
    # if sale_price:
    #     subtotal = sale_price * quantity
    # else:
    #     subtotal = price * quantity

    # return subtotal

    return price * quantity

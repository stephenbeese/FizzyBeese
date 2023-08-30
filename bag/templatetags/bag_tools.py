from django import template

register = template.Library()


@register.filter(name='calculate_subtotal')
def calculate_subtotal(price, quantity):
    """ function to calculate a products subtotal in the bag """
    return price * quantity

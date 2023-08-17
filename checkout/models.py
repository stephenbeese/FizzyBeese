import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total_weight = models.IntegerField(null=False, default=0)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')


    def _generate_order_number(self):
        """
        Generate an order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time
        """
        # self.order_total = self.lineitems.aggregate(sum('lineitem_total'))['lineitem_total__sum']
        self.total_weight = self.lineitems.aggregate(sum_weight=Sum('product__weight', output_field=models.IntegerField()))['sum_weight'] or 0

        order_total = Decimal('0.00')
        for line_item in self.lineitems.all():
            order_total += line_item.lineitem_total


        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            if self.total_weight <= 100:
                self.delivery_cost = Decimal('1.60')
            elif self.total_weight <= 2000:
                self.delivery_cost = Decimal('3.69')
            else:
                self.delivery_cost = Decimal('5.29')
        else:
            self.delivery_cost = Decimal('0.00')
        
        self.order_total = order_total
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method
        Set the order number if one hasn't been set
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method 
        Set the lineitem total and update order total
        """
        if self.product.sale_price:
            self.lineitem_total = self.product.sale_price * self.quantity
        else:
            self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
 
    def __str__(self):
        return f'product {self.product.name} on order {self.order.order_number}'

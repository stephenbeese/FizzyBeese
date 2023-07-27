from django.db import models


class Category(models.Model):
    """ A model to store the categories for filtering """

    class Meta:
        abstract = True

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class ProductCategory(Category):
    """ A model to store the product categories for filtering """

    class Meta:
        verbose_name_plural = 'Product Categories'


class FragranceCategory(Category):
    """ A model to store all fragrance types for filtering """

    class Meta:
        verbose_name_plural = 'Fragrance Categories'


class Product(models.Model):
    """ A model to store all product data """
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_remaining = models.IntegerField(null=False)
    product_categories = models.ManyToManyField(ProductCategory)  # Links to ProductCategory
    fragrance_categories = models.ManyToManyField(FragranceCategory, null=True, blank=True)  # Links to FragranceCategory
    weight = models.IntegerField()
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_clearance = models.BooleanField()
    is_featured = models.BooleanField()
    is_hidden = models.BooleanField()
    image = models.ImageField(null=True, blank=True)
    label_image = models.ImageField(null=True, blank=True)
    uploaded_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class AdditionalImages(models.Model):
    """ stores additional images for products that have them """
    product_id = models.ForeignKey('Product', null=False, blank=False, on_delete=models.CASCADE)
    image = models.ImageField()

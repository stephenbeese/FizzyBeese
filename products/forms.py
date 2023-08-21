from django import forms
from .models import Product, ProductCategory, FragranceCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fragrance_categories = FragranceCategory.objects.all()
        product_categories = ProductCategory.objects.all()
        fragrance_friendly_names = [(f.id, f.get_friendly_name()) for f in fragrance_categories]
        product_friendly_names = [(p.id, p.get_friendly_name()) for p in product_categories]

        self.fields['fragrance_categories'].choices = fragrance_friendly_names
        self.fields['product_categories'].choices = product_friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black'

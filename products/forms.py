from django import forms
from .models import Product, ProductCategory, FragranceCategory, AdditionalImages


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['uploaded_on']
        labels = {
            'price': 'Price (£)',
            'product_categories': 'Product categories (Hold "ctrl" or "cmd" to select more than one)',
            'fragrance_categories': 'Fragrance categories (Hold "ctrl" or "cmd" to select more than one)',
            'weight': 'Weight (g)',
            'sale_price': 'Sale Price (£)',
        }

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


class AdditionalImagesForm(forms.ModelForm):
    class Meta:
        model = AdditionalImages
        fields = ['image']

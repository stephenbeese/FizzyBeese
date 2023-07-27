from django.contrib import admin
from .models import Product, ProductCategory, FragranceCategory, AdditionalImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'stock_remaining',
        'is_clearance',
        'is_featured',
        'is_hidden',
        'uploaded_on',
    )

    ordering = ('uploaded_on',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


@admin.register(FragranceCategory)
class FragranceCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


@admin.register(AdditionalImages)
class AdditionalImagesAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'image',
    )

    ordering = ('product_id',)


# admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductCategory, ProductCategoryAdmin)
# admin.site.register(FragranceCategory, FragranceCategoryAdmin)
# admin.site.register(AdditionalImages, AdditionalImagesAdmin)

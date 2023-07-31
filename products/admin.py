from django.contrib import admin
from .models import Product, ProductCategory, FragranceCategory, AdditionalImages
from import_export.admin import ImportExportModelAdmin


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = (
        'name',
        'price',
        'stock_remaining',
        'sale_price',
        'is_clearance',
        'is_featured',
        'is_hidden',
        'uploaded_on',
    )

    ordering = ('uploaded_on',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'friendly_name',
        'name',
    )


@admin.register(FragranceCategory)
class FragranceCategoryAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
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

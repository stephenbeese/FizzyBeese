from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.all_products,
        name='products'),
    path(
        '<int:product_id>/',
        views.product_detail,
        name='product_detail'),
    path(
        'add/',
        views.add_product,
        name='add_product'),
    path(
        'edit/<int:product_id>/',
        views.edit_product,
        name='edit_product'),
    path(
        'delete/<int:product_id>/',
        views.delete_product,
        name='delete_product'),
    path(
        'add_image/<int:product_id>/',
        views.add_image,
        name='add_image'),
    path(
        'delete_additional_image/<int:image_id>/',
        views.delete_additional_image,
        name='delete_additional_image'),
    path(
        'hidden/',
        views.hidden_products,
        name='hidden_products'),
]

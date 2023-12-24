from django.contrib import admin
from django.urls import path
from cart_management import views

app_name = 'cart_mng'

urlpatterns = [
    path('cart/', views.cart, name ='cart'),
    path('add-cart/<int:id>/', views.add_cart, name ='add_cart'),
    path('ajax/update/cart/', views.newcart_update, name='newcart_update'),
    path('ajax/remove/cart/', views.remove_cart_item_fully, name='remove_cart_item_fully'),
    path('remove-cart-item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
]

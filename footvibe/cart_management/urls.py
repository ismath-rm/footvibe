from django.contrib import admin
from django.urls import path
from cart_management import views

app_name = 'cart_mng'

urlpatterns = [
    path('cart/', views.cart, name ='cart'),
    path('add-cart/<int:id>/', views.add_cart, name ='add_cart'),
    # path('remove-cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove-cart-item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),]

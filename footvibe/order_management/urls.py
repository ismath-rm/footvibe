from django.contrib import admin
from django.urls import path
from order_management import views


app_name = 'order_mng'

urlpatterns = [
    path('order_placed/', views.order_placed, name='order_placed'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('payment/', views.payment, name='payment'),
    path('ordered_detail/<int:order_id>/', views.ordered_detail, name='ordered_detail'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('update_status/', views.update_status, name='update_status'),

]

from django.contrib import admin
from django.urls import path
from order_management import views


app_name = 'order_mng'

urlpatterns = [
    path('order_placed/', views.order_placed, name='order_placed'),
    # path('order/<int:order_id>/', views.order, name='order'),

]

from django.urls import path
from order_management import views


app_name = 'order_mng'

urlpatterns = [
    path('order_placed/', views.order_placed, name='order_placed'),
    path('payment/', views.payment, name='payment'),
    path('ordered_detail/<int:order_id>/', views.ordered_detail, name='ordered_detail'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
     path('return_order/<int:order_id>/',views.return_order,name='return_order'),

]

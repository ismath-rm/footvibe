from django.urls import path
from admin_side import views

app_name='admin_log'

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
   
    path('order_list/',views.order_list,name='order_list'),
    path('user_list/',views.user_list,name='user_list'),
    path('block_unblock_user/<int:user_id>/',views.block_unblock_user,name='block_unblock_user'),
]

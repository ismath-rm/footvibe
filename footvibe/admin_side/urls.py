from django.urls import path
from admin_side import views

app_name='admin_log'

urlpatterns = [

    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('sales_report',views.sales_report,name='sales_report'),

    path('order_list',views.order_list,name='order_list'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
    # path('cancell_order/<int:order_id>/',views.cancell_order,name='cancell_order'),

    path('user_list/',views.user_list,name='user_list'),
    path('block_unblock_user/<int:user_id>/',views.block_unblock_user,name='block_unblock_user'),

    path('coupon/', views.AdminCoupon.as_view(), name='coupon'),
    path('generate_code/', views.generate_code, name='generate_code'),
    path('delete_coupon/<int:id>/', views.delete_coupon, name='delete_coupon'),

    path('home_main_slider/', views.home_main_slider, name='home_main_slider'),
    path('delete_slide/<int:slide_id>', views.delete_slide, name='delete_slide'),

]

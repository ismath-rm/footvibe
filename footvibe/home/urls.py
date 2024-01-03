from django.contrib import admin
from django.urls import path
from home import views

app_name = 'log'

urlpatterns = [
   path('', views.index,name='index'),
   path('user_login', views.user_login,name='user_login'),
   path('user_signup', views.user_signup,name='user_signup'),
   path('user_logout', views.user_logout,name='user_logout'),

#........................................................Otp.............................................................#

   path('send_otp/', views.send_otp, name= 'send_otp'),
   path('verify_otp/', views.verify_otp,name='verify_otp'),

#....................................................Forgot password.....................................................#

   path('forgot_password/', views.forgot_password,name='forgot_password'),
   path('sent_otp_forgot_password/', views.sent_otp_forgot_password,name='sent_otp_forgot_password'),
   path('verify_otp_forgot_password/', views.verify_otp_forgot_password,name='verify_otp_forgot_password'),
   path('resend/', views.resend_otp,name='resend_otp'),
   

   path('product_detail/<slug:variant_slug>/', views.product_detail, name='product_detail'),

   
   path('shop/', views.shop, name = 'shop'),
   path('shop_category/<slug:slug>', views.shop_category, name='shop_category'),

#...................................................Profile..............................................................#

   path('user_profile/', views.user_profile, name='user_profile'),
   path('add_address/<str:source>/', views.add_address, name='add_address'),
   path('edit_profile/', views.edit_profile, name='edit_profile'),
   path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
   path('set_default_address/<int:address_id>/', views.set_default_address, name='set_default_address'),

   #.....................................checkout..............................................#

   path('checkout/', views.checkout, name='checkout'),


]
from django.contrib import admin
from django.urls import path
from home import views

app_name = 'log'

urlpatterns = [
   path('',views.index,name='index'),
   path('user_login',views.user_login,name='user_login'),
   path('user_signup',views.user_signup,name='user_signup'),
   path('user_logout',views.user_logout,name='user_logout'),

   path('send_otp',views.send_otp, name= 'send_otp'),
   path('verify_otp',views.verify_otp,name='verify_otp'),

   path('forgot_password',views.forgot_password,name='forgot_password'),
   path('sent_otp_forgot_password',views.sent_otp_forgot_password,name='sent_otp_forgot_password'),
   path('verify_otp_forgot_password',views.verify_otp_forgot_password,name='verify_otp_forgot_password'),
   path('resend',views.resend_otp,name='resend_otp'),
   
   path('product_detail/<slug:variant_slug>', views.product_detail, name='product_detail'),
   
]
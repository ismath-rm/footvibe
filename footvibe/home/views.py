from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Account
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
import random,re
from django.core.exceptions import ObjectDoesNotExist
from product_management.models import *


# Create your views here.
    
def index(request):
    variants = []
    products = Product.objects.filter(is_active = True)

    for product in products:
        prod_variants = ProductVariant.objects.filter(product = product, is_active = True)
        if prod_variants:
            variants.append(prod_variants[0])
    context = {
        'products': variants,
    }

    return render(request, 'user/index.html',context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('log:index')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
     

        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in successfully')
            return redirect('log:index')
        
        if not Account.objects.filter(email=email).exists():
            messages.error(request,"There is not such a user")
            return redirect('log:user_login')
        if Account.objects.filter(email=email,is_active=False).exists():
            messages.error(request,"You are Blocked By Admin, Please contact Admin")
            return redirect('log:user_login')
        else:
            messages.error(request, 'Login failed. Please check your email and password.')

    return render(request, 'user/user_login.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('log:index')
    
    if request.method=='POST':
        user=request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        print('email',email)
        print('pass',password)
        
        if  Account.objects.filter(username=user).exists():
            messages.error(request, "Username already existing")
            return redirect('log:user_signup')
        

        if  Account.objects.filter(email=email).exists():
            messages.error(request, "Email Address already existing")
            return redirect('log:user_signup')
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Invalid email")
            return redirect('log:user_signup')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('log:user_signup')
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('log:user_signup')
        
        user=Account.objects.create_user(email=email, password=password,username=user)
        user.save()

        # Add success message
        messages.success(request, 'Signup successful. Please check your email for OTP verification.')



        request.session['email']=email
        return redirect('log:send_otp')
        

    else:
        
        return render(request,'user/user_signup.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def send_otp(request):

    random_num=random.randint(1000,9999)
    request.session['OTP_Key']=random_num


    send_mail(
        "OTP AUTHENTICATING footvibe",
        f"{random_num} -OTP",
        "ismathrm9@gmail.com",
        [request.session['email']],
        fail_silently=False,
    )

    print(random_num)
    return redirect('log:verify_otp')

def verify_otp(request):
    print('hiii')
    user=Account.objects.get(email=request.session['email'])
    if request.method=="POST":

        if str(request.session['OTP_Key']) != str(request.POST['otp']):
            print(request.session['OTP_Key'],request.POST['otp'])
            messages.error(request, "wrong OTP. Please enter the correct OTP")

        else:
            user.is_active=True
            user.save()
            # login(request,user)
            print("helo")
            messages.success(request, "OTP has been verified successfully!")
            return redirect('log:user_login')
            
    return render(request,'user/otp_verification.html')


@login_required(login_url='log:user_login')
def user_logout(request):
    logout(request)
    messages.success(request, "your logout is successfull")
    return redirect('log:index')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_password(request):
    if request.method == "POST":

        email=request.POST["email"]
        pass1=request.POST["password"]
        pass2=request.POST["conform_password"]

        if pass1 != pass2:
            messages.error(request,"Passwords do not match.")
            return redirect('user_log/forgot_password.html')
        try:
            user = Account.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.warning(request, "your user email not available, plese enter a valid email")
        request.session['email']=email
        request.session['password']=pass1
        return redirect('log:sent_otp_forgot_password') 
    else:
         return render(request,'user/forgot_password.html')
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sent_otp_forgot_password(request):
   random_num=random.randint(1000,9999)
   print(random_num)
   request.session['OTP_Key']=random_num
   send_mail(
   "OTP AUTHENTICATING footvibe",
   f"{random_num} -OTP",
   "ismathrm9@gmail.com",
   [request.session['email']],
   fail_silently=False,
    )
   return redirect('log:verify_otp_forgot_password')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verify_otp_forgot_password(request):
    user=Account.objects.get(email=request.session['email'])

    if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         print(request.session['OTP_Key'],request.POST['otp'])
         messages.error(request, "wrong OTP. Please enter the correct OTP")
         return redirect('log:verify_otp_forgot_password')
      else:
         password=request.session['password']
         user.set_password(password)
         user.save()
         login(request,user)
         messages.success(request, "Password changed successfully!")
         return redirect('log:user_login')
    return render(request,'user/otp_verification.html')



def resend_otp(request):
    
    
    random_num=random.randint(1000,9999)
    print(random_num)
    request.session['OTP_Key']=random_num
    send_mail(
    "OTP AUTHENTICATING footvibe",
    f"{random_num} -OTP",
    "ismathrm9@gmail.com",
    [request.session['email']],
    fail_silently=False,
    )
    messages.success(request, "OTP has been resent successfully!")
    return redirect('log:verify_otp')





def product_detail(request, variant_slug):
    print('hello', variant_slug)
    try:
        single_product = ProductVariant.objects.get(product_variant_slug = variant_slug)

    except Exception as e:
        print(e)

    product_images = [image.image for image in single_product.product_images.all()]
    product_images.insert(0, single_product.thumbnail_image)
    

    context = {
        'single_product': single_product,
        'product_images': product_images,
    }        


    return render(request,'user/product_detail.html',context)
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from home.models import *
from django.contrib.auth import login,logout,authenticate
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from order_management.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from order_management.forms import OrderForm 
from datetime import timedelta, datetime
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear,TruncDate
from django.http import JsonResponse
import random
import string
from django.views import View
from admin_side.models import *
from home.forms import *


# Create your views here. 

def superadmin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Invalid admin credentials!")
            return redirect('admin_log:admin_login')
    return _wrapped_view


@login_required(login_url='admin_log:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@superadmin_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')

    product_count = Product.objects.count()
    category_count = Category.objects.count()
    orders = Order.objects.all()
    last_orders = Order.objects.order_by('-created_at')[:5]
    orders_count = orders.count()
    total_users_count = Account.objects.count()
    total = 0
    total_del = 0
    total_raz = 0
    total_wallet = 0


    for order in orders:
        
        if order.status == 'Delivered':
            total_del += order.order_total
                  
        if order.payment and (order.payment.payment_method == 'RAZORPAY' or order.payment.payment_method == 'Wallet') and not order.status == 'Cancelled':
            print(f'payment method:{order.payment.payment_method} order status: {order.status} order total:{order.order_total}')
            # total_raz += order.order_total
            if order.payment.payment_method == 'RAZORPAY':
                total_raz += order.order_total
            elif order.payment.payment_method == 'Wallet':
            # Handle Wallet payments
                total_wallet += order.order_total
       
  
    revenue = total_del + total_raz
   
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    daily_order_counts = (
        Order.objects
        .filter(created_at__range=(start_date, end_date), is_ordered=True)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(order_count=Count('id'))
        .order_by('date')
    )

    print(daily_order_counts)
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in daily_order_counts]
    counts = [entry['order_count'] for entry in daily_order_counts]

    monthly_order_counts = (
        Order.objects
        .filter(created_at__year=datetime.now().year)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(order_count=Count('id'))
        .order_by('month')
    )
    monthlyDates = [entry['month'].strftime('%Y-%m') for entry in monthly_order_counts]
    monthlyCounts = [entry['order_count'] for entry in monthly_order_counts]

    yearly_order_counts = (
        Order.objects
        .annotate(year=TruncYear('created_at'))
        .values('year')
        .annotate(order_count=Count('id'))
        .order_by('year')
    )
    yearlyDates = [entry['year'].strftime('%Y') for entry in yearly_order_counts]
    yearlyCounts = [entry['order_count'] for entry in yearly_order_counts]

    statuses = ['Delivered', 'New', 'Conformed', 'Cancelled', 'Return', 'Shipped']
    order_counts = [Order.objects.filter(status=status).count() for status in statuses]

    context = {
        'product_count': product_count,
        'category_count': category_count,
        'orders_count': orders_count,
        'dates': dates,
        'counts': counts,
        'monthlyDates': monthlyDates,
        'monthlyCounts': monthlyCounts,
        'yearlyDates': yearlyDates,
        'yearlyCounts': yearlyCounts,
        'last_orders': last_orders,
        'revenue': revenue,
        'total_users_count': total_users_count,
        'statuses': statuses,
        'order_counts': order_counts,
    }

    return render(request, 'admin_temp/index.html', context)






@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    print("hiii")
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_log:dashboard')

    
    if request.method == 'POST':
        user_email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=user_email, password=password)
        print("helloooooooooo")

        if user:
            if user.is_superuser:
                login(request, user)
                messages.success(request, 'You are logged in successfully')
                return redirect('admin_log:dashboard')
        
        else:
            messages.error(request, 'Login failed. Please check your email and password.')


    return render(request,'admin_temp/admin_login.html')



@login_required(login_url='admin_log:admin_login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):

    logout(request)

    return redirect('admin_log:admin_login')


#....................................order.......................................#


@login_required(login_url='admin_log:admin_login')  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_list(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    status = 'all'
    orders = Order.objects.order_by('-created_at')

    if request.method == 'POST':
        status = request.POST.get('status', 'all')
        if status != 'all':
            orders = orders.filter(status=status)

    paginator = Paginator(orders, 10)
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'orders': orders,
        'status': status,
    }

    return render(request, 'admin_temp/order_list.html', context)




# @login_required(login_url='admin_log:admin_login')  
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def order_detail(request, order_id):
#     print('ypoooooo')
#     try:
#         order = Order.objects.get(id=order_id)
#     except Order.DoesNotExist:
#         return HttpResponse("Order not found")

#     ordered_products = OrderProduct.objects.filter(order=order)

#     tax = (2 * order.order_total) / 100

#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             print(form)
#             messages.success(request, 'Changes saved successfully.')
#             return redirect('admin_log:order_list')  
#     else:
#         form = OrderForm(instance=order)
#     context = {
#         'order': order,
#         'ordered_products': ordered_products,
#         'total': sum(item.get_total for item in ordered_products),
#         'tax': tax,
#         'subtotal':int(order.order_total-tax),
#         'grand_total': order.order_total + tax,
#         'form': form,
#     }

#     return render(request, 'admin_temp/order_detail.html', context)


# @login_required(login_url='admin_log:admin_login')  
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def order_detail(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#     except Order.DoesNotExist:
#         return HttpResponse("Order not found")

#     ordered_products = OrderProduct.objects.filter(order=order)

#     tax = (2 * order.order_total) / 100

#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()

#             # Check for cancellation and process accordingly
#             if order.status == 'Cancelled' and order.payment:
#                 if order.payment.payment_method in ['RAZORPAY', 'Wallet']:
#                     order.payment.status = 'Cancelled'
#                     order.payment.save()

#                     wallet, created = Wallet.objects.get_or_create(user=order.user)
#                     if order.order_total > 0:
#                         wallet.balance += order.order_total
#                         print(f"Before balance update: {wallet.balance}")
#                         wallet.save()
#                         print(f"After balance update: {wallet.balance}")

#                         WalletHistory.objects.create(
#                             wallet=wallet,
#                             type='Credited',
#                             amount=order.order_total
#                         )
                        
#                         # Debugging print statements
#                         print(f"Order {order.id} has been cancelled. Amount of {order.order_total} credited to the wallet.")

#                         wallet_history_entries = WalletHistory.objects.filter(wallet=wallet)
#                         for entry in wallet_history_entries:
#                             print(f"Wallet history entry: {entry.type} - {entry.amount}")

                        
#                         messages.success(request, f'Order {order.id} has been cancelled. Amount of {order.order_total} credited to your wallet.')
#                     else:
#                         # Debugging print statements
#                         print(f"Order {order.id} has been cancelled. No amount to credit.")
#                         messages.success(request, f'Order {order.id} has been cancelled.')
#                 elif order.payment.payment_method == 'CashOnDelivery':
#                     # Debugging print statements
#                     print(f'Cash on Delivery order {order.id} has been cancelled.')
#                     messages.success(request, f'Cash on Delivery order {order.id} has been cancelled.')
#                 else:
#                     # Debugging print statements
#                     print("Invalid payment method")
#                     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#             messages.success(request, 'Changes saved successfully.')
#             return redirect('admin_log:order_list')          
#     else:
#         form = OrderForm(instance=order)

#     context = {
#         'order': order,
#         'ordered_products': ordered_products,
#         'total': sum(item.get_total for item in ordered_products),
#         'tax': tax,
#         'subtotal': int(order.order_total - tax),
#         'grand_total': order.order_total + tax,
#         'form': form,
#     }

#     return render(request, 'admin_temp/order_detail.html', context)





@login_required(login_url='admin_log:admin_login')  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Order not found")

    ordered_products = OrderProduct.objects.filter(order=order)

    tax = (2 * order.order_total) / 100

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

            # Check for cancellation and process accordingly
            if order.status == 'Cancelled' and order.payment:
                if order.payment.payment_method in ['RAZORPAY', 'Wallet']:
                    order.payment.status = 'Cancelled'
                    order.payment.save()

                    wallet, created = Wallet.objects.get_or_create(user=order.user)
                    if order.order_total > 0:
                        wallet.balance += order.order_total
                        print(f"Before balance update: {wallet.balance}")
                        wallet.save()
                        print(f"After balance update: {wallet.balance}")

                        WalletHistory.objects.create(
                            wallet=wallet,
                            type='Credited',
                            amount=order.order_total
                        )
                        
                        # Debugging print statements
                        print(f"Order {order.id} has been cancelled. Amount of {order.order_total} credited to the wallet.")

                        wallet_history_entries = WalletHistory.objects.filter(wallet=wallet)
                        for entry in wallet_history_entries:
                            print(f"Wallet history entry: {entry.type} - {entry.amount}")

                        
                        messages.success(request, f'Order {order.id} has been cancelled. Amount of {order.order_total} credited to your wallet.')
                    else:
                        # Debugging print statements
                        print(f"Order {order.id} has been cancelled. No amount to credit.")
                        messages.success(request, f'Order {order.id} has been cancelled.')
                elif order.payment.payment_method == 'CashOnDelivery':
                    # Debugging print statements
                    print(f'Cash on Delivery order {order.id} has been cancelled.')
                    messages.success(request, f'Cash on Delivery order {order.id} has been cancelled.')
                else:
                    # Debugging print statements
                    print("Invalid payment method")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            # Check for return and process accordingly
            if order.status == 'Returned' and order.payment:
                if order.payment.payment_method in ['RAZORPAY', 'Wallet']:
                    order.payment.status = 'Returned'
                    order.payment.save()
                    
                    wallet, created = Wallet.objects.get_or_create(user=order.user)
                    if order.order_total > 0:
                        wallet.balance += order.order_total
                        print(f"Before retrun balance update: {wallet.balance}")
                        wallet.save()
                        print(f"After return balance update: {wallet.balance}")

                        WalletHistory.objects.create(
                            wallet=wallet,
                            type='Credited',
                            amount=order.order_total
                        )
                        
                        # Debugging print statements
                        print(f'Order {order.id} has been returned. Amount of {order.order_total} credited to your wallet.')

                        wallet_history_entries = WalletHistory.objects.filter(wallet=wallet)
                        for entry in wallet_history_entries:
                            print(f"Wallet history entry: {entry.type} - {entry.amount}")

                        
                        messages.success(request, f'Order {order.id} has been returned. Amount of {order.order_total} credited to your wallet.')
                    else:
                        # Debugging print statements
                        print(f'Order {order.id} has been returned. No amount to credit.')
                        messages.success(request, f'Order {order.id} has been returned.')
                
                else:
                    # Debugging print statements
                    print("Invalid payment method for return")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            messages.success(request, 'Changes saved successfully.')
            return redirect('admin_log:order_list')          
    else:
        form = OrderForm(instance=order)

    context = {
        'order': order,
        'ordered_products': ordered_products,
        'total': sum(item.get_total for item in ordered_products),
        'tax': tax,
        'subtotal': int(order.order_total - tax),
        'grand_total': order.order_total + tax,
        'form': form,
    }

    return render(request, 'admin_temp/order_detail.html', context)





# @login_required(login_url='admin_log:admin_login')  
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def cancell_order(request, order_id):
#     if not request.user.is_superuser:
#         return redirect('admin_log:admin_login')
    
#     try:
#         order = Order.objects.get(id=order_id)
#     except Order.DoesNotExist:
#         messages.error(request, "Order does not exist")
#         return redirect('admin_log:order_list')

#     order.status = 'Cancelled'
#     order.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



#......................................user list........................................#


@login_required(login_url='admin_log:admin_login')  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_log:admin_login')
    
    search_query=request.GET.get('query')

    if search_query:
         users = Account.objects.filter(username__icontains=search_query)
    else:
         users = Account.objects.filter(is_staff = False)
         print("the users are :", users)
    context = {
        'users': users
    }
      
    return render(request,'admin_temp/user_list.html',context)


@login_required(login_url='admin_log:admin_login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_unblock_user(request,user_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    user = get_object_or_404(Account, id=user_id)
    
    if user.is_active:
        user.is_active=False
        
    else:
        user.is_active=True
        
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class AdminCoupon(View):
    template_name = "admin_temp/coupon.html"

    def get(self, request, *args, **kwargs):
        coupons = Coupon.objects.all()
        context = {
            'coupons': coupons,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        coupon_code = request.POST.get("couponcode")
        discount_amount = request.POST.get("discount")
        minimum_amount = request.POST.get("minimumAmount")
        valid_to = request.POST.get("couponexpiry")


        if Coupon.objects.filter(coupon_code=coupon_code).exists():
            messages.warning(request,"Coupon Code is Alredy Exist")
            coupons = Coupon.objects.all()
            return render(request, self.template_name, {"coupons": coupons, "error": "Duplicate coupon code"})

        coupon = Coupon.objects.create(
            coupon_code=coupon_code,
            discount=discount_amount,
            minimum_amount=minimum_amount,
            valid_to=valid_to
        )
        
        messages.success(request, f"Coupon '{coupon.coupon_code}' created successfully!")

        coupons = Coupon.objects.all()
        return redirect("admin_log:coupon")



def generate_code(request):
  alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
  code = ''.join(random.choice(alphabet) for i in range(8))
  

  return JsonResponse({'code': code})
  

def delete_coupon(request,id):
    
    coupon = get_object_or_404(Coupon, id=id)
    coupon.delete()
    messages.success(request, f"Coupon '{coupon.coupon_code}' deleted successfully!")
    return redirect("admin_log:coupon") 

    







def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')

    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')

    start_date_value = ""
    end_date_value = ""

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date

        try:
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                orders = orders.filter(created_at__range=(start_date, end_date))
        except ValueError as e:
            print(f"Error: {e}")

    # Annotate orders with total_quantity
    orders = orders.annotate(
        total_quantity=Sum('orderproduct__quantity')
    )

    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        orders = paginator.page(paginator.num_pages)

    context = {
        'orders': orders,
        'start_date_value': start_date_value,
        'end_date_value': end_date_value
    }

    return render(request, 'admin_temp/sales_report.html', context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_main_slider(request):
     if not request.user.is_superuser:
          return redirect ('admin_log:admin_login')
     if request.method=='POST':
          form=HomeMainSliderForm(request.POST, request.FILES)
          if form.is_valid():
               form.save()
               return redirect('admin_log:home_main_slider')
     else:

          form= HomeMainSliderForm
     list=HomeMainSlide.objects.all()
     return render(request,'admin_temp/banner.html',{'form':form,'list':list})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_slide(request, slide_id):
    if not request.user.is_superuser:
         return redirect ('admin_log:admin_login')
    try:
        slide_to_delete = HomeMainSlide.objects.get(pk=slide_id)
        slide_to_delete.delete()
    except HomeMainSlide.DoesNotExist:
        # Handle the case where the slide with the given ID does not exist.
        pass

    return redirect('admin_log:home_main_slider')

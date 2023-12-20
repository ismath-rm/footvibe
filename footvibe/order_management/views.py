from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from order_management.models import *
from cart_management.models import *
from home.models import *
from datetime import datetime
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

@login_required(login_url='log:user_login')
def order_placed(request, total=0, quantity=0):
    if not request.user.is_authenticated:
        return redirect('log:index')

    current_user = request.user
    cart_items = CartItem.objects.filter(cart__user=current_user)

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product_variant.sale_price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty. Add items to your cart before placing an order.')
        return redirect('log:cart')

    if request.method == 'POST':
        selected_payment_option = request.POST.get('payment_option')

        try:
            address = AddressBook.objects.get(user=request.user, is_default=True)
        except AddressBook.DoesNotExist:
            messages.warning(request, 'No delivery address exists! Add an address and try again')
            return redirect('log:checkout')

        data = Order()
        data.user = current_user
        data.first_name = address.first_name
        data.last_name = address.last_name
        data.phone = address.phone
        data.email = address.email
        data.address_line_1 = address.address_line_1
        data.city = address.city
        data.state = address.state
        data.country = address.country
        data.pincode = address.pincode
        data.order_total = grand_total
        data.order_total = total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()

        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.is_ordered = True
        data.save()

        payment_id = f'uw{data.order_number}{data.id}'
        payment_status = 'COMPLETED' if selected_payment_option == 'CashOnDelivery' else 'Pending'
        payment = Payment.objects.create(
            user=current_user, 
            payment_method=selected_payment_option,
            payment_id=payment_id,
            amount_paid=data.order_total,
            status=payment_status
        )
        payment.save()
        data.payment = payment
        data.save()

        ordered_products = []

        for cart_item in cart_items:
            ordered_product = OrderProduct.objects.create(
                user=current_user,
                order=data,
                payment=payment,
                product=cart_item.product_variant.product,
                product_price=cart_item.product_variant.sale_price,
                quantity=cart_item.quantity,
                is_ordered=True,
            )
            ordered_products.append(ordered_product)

        cart_items.delete()
        context = {
            'order': data,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
            'ordered_products': ordered_products,
        }

        if selected_payment_option == "CashOnDelivery":
            print("Selected Payment Method:", selected_payment_option)
            return render(request, "user/order_placed.html", context)

        elif selected_payment_option == "RAZORPAY":
            # Additional logic for Razorpay payment
            return render(request, "user/payment.html", context)

    return redirect('log:checkout')





def payment(request):
    current_user = request.user
    payment_method = request.GET.get('method')
    payment_id = request.GET.get('payment_id')
    # payment_order_id = request.GET.get('payment_order_id')
    order_id = request.GET.get('order_id')


  
    if not current_user.is_authenticated:
        return HttpResponse("User must be logged in for online payment")

    # Get order details
    try:
        order = Order.objects.get(order_number=order_id, user=current_user)
    except Order.DoesNotExist:
        return HttpResponse("Order not found")

    # Get ordered products for the order
    ordered_products = OrderProduct.objects.filter(order=order)

    # Calculate total amount (you might need to adjust this based on your models)
    total_amount = order.order_total

    # You can pass additional context data if needed
    context = {
        'order': order,
        'ordered_products': ordered_products,
        'total_amount': total_amount,
        'payment_method':payment_method,
        'payment_id':payment_id,
        
    }

    return render(request, "user/order_placed.html", context)


@login_required(login_url='log:user_login')
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if order.status == 'Delivered':
        # Update the order status to 'Cancelled'
        order.status = 'Cancelled'
        order.save()

        # Optional: Implement stock adjustments if needed
        # Example: Increment stock for variations
        for order_product in order.orderproduct_set.all():
            if order_product.variations.exists():
                for variation in order_product.variations.all():
                    variation.stock += order_product.quantity
                    variation.save()

        messages.warning(request, 'Cancel request has been sent.')

    else:
        messages.warning(request, 'Cancel request cannot be processed.')

    return redirect('log:my_order')




def ordered_detail(request, order_id):
    current_user = request.user

    try:
        order = Order.objects.get(id=order_id, user=current_user)
    except Order.DoesNotExist:

        return HttpResponse("Order not found")

    ordered_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'ordered_products': ordered_products,

    }
    return render(request, 'user/order_detail.html', context)






@login_required(login_url='log:user_login')
def my_orders(request):

    if not request.user.is_authenticated:
        return redirect('log:index')
    
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    order_products = OrderProduct.objects.filter(order__in=orders)
    context = {
        'orders': orders,
        "order_products":order_products
    }
  
    return render(request, 'user/order.html', context)




def update_status(request):
    if request.method == "POST":
        order_id = request.POST.get('OrderID')
        status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)

        # Update the order status
        order.status = status
        order.save()
        print(order.status, order.order_number)
    # return redirect('orders:admn_product_order')
        return redirect('log:order')






from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from order_management.models import *
from cart_management.models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.



# @login_required(login_url='log:user_login')
# def order_placed(request, total=0, quantity=0):
#     if not request.user.is_authenticated:
#         return redirect('log:index')
    
#     current_user = request.user

#     # If the cart count is less than or equal to 0, then redirect back to home
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('log:index')

#     grand_total = 0
#     tax = 0
    
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (2 * total)/100

#     grand_total = total + tax 
    
#     if request.method == 'POST':
#         try:
#             address = AddressBook.objects.get(user=request.user, is_default=True)
#         except AddressBook.DoesNotExist:
#             messages.warning(request, 'No delivery address exists! Add an address and try again')
#             return redirect('log:checkout')
        
#         # Create an Order instance
#         order = Order.objects.create(
#             user=current_user,
#             first_name=address.first_name,
#             last_name=address.last_name,
#             phone=address.phone,
#             email=address.email,
#             address_line_1=address.address_line_1,
#             address_line_2=address.address_line_2,
#             city=address.city,
#             state=address.state,
#             country=address.country,
#             pincode=address.pincode,
#             order_total=grand_total,
#             tax=tax,
#             ip=request.META.get('REMOTE_ADDR'),
#         )

#         # Generate order number
#         yr = int(datetime.date.today().strftime('%Y'))
#         dt = int(datetime.date.today().strftime('%d'))
#         mt = int(datetime.date.today().strftime('%m'))
#         d = datetime.date(yr, mt, dt)
#         current_date = d.strftime("%Y%m%d")
#         order_number = current_date + str(order.id)
#         order.order_number = order_number
#         order.save()

#         context = {
#             'order': order,
#             'cart_items': cart_items,
#             'total': total,
#             'tax': tax,
#             'grand_total': grand_total,
#         }

#         return render(request, 'user_/payment.html', context)
#     else:
#         return redirect('user:checkout')


def order_placed(request):
    print('order placed succussfully')

    return render(request,'user/order_placed.html')



# def order(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'user/order_detail.html', {'order': order})
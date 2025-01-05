from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, ExpressionWrapper
from django.contrib import messages
from cart_management.models import *
from product_management.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.http import JsonResponse, HttpResponseBadRequest



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=request.user)
            active_carts = Cart.objects.filter(cartitem__in=cart_items).distinct()

            cart_items = CartItem.objects.filter(cart__in=active_carts)

            for cart_item in cart_items:
                total += (cart_item.product_variant.sale_price * cart_item.quantity)
                quantity += cart_item.quantity

            tax = (2 * total) / 100
            grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total, 
    }

    return render(request, 'user/cart.html', context)



# def add_cart(request, id):
#     color = request.POST.get('color')
#     size = request.POST.get('size')
#     qyt = request.POST.get('input')
#     qyt = int(qyt)
#     print(color)
#     print(size)
#     try:
#         id = Product.objects.get(id=id)
#         print(id)
#         product_variant = ProductVariant.objects.filter(
#             product=id,
#             attribute_value__attribute__attribute_name__in=['color', 'size'],
#             attribute_value__attribute_value__in=[color, size]
#         ).first()
#         print(product_variant)
#         if product_variant.stock >= 1:
#             if request.user.is_authenticated:
#                 is_cart_item_exists = CartItem.objects.filter(
#                     cart__user=request.user,
#                     product_variant=product_variant
#                 ).exists()

#                 if is_cart_item_exists:
#                     cart_item = CartItem.objects.get(
#                         cart__user=request.user,
#                         product_variant=product_variant,
#                     )

#                     if qyt < product_variant.stock:
#                         cart_item.quantity += qyt
#                         cart_item.save()
#                         messages.success(request, "Item quantity updated.")
#                     else:
#                         messages.success(request, "Product out of stock")
#                 else:
#                     cart, created = Cart.objects.get_or_create(user=request.user)
#                     CartItem.objects.create(cart=cart, product_variant=product_variant, quantity=qyt)
#                     messages.success(request, "Item added to the cart.")
#                     return redirect('cart_mng:cart')
#             else:
#                 messages.success(request, "Please login to purchase")
#                 return redirect('log:user_login')
#         else:
#             messages.warning(request, 'This item is out of stock.')
#             return redirect('log:product_detail', id)
#     except ProductVariant.DoesNotExist:
#         messages.warning(request, 'Variation not available, please select another variation')
#     except Exception as e:
#         print(f"The error is {e}")

#     return redirect('cart_mng:cart')

def add_cart(request, id):
    color = request.POST.get('color')
    size = request.POST.get('size')
    qyt = request.POST.get('input')
    qyt = int(qyt)
    print(f"Color: {color}, Size: {size}, Quantity: {qyt}")
    try:
        product = Product.objects.get(id=id)
        
        # Check if product_variant exists based on the selected color and size
        product_variant = ProductVariant.objects.filter(
            product=product,
            attribute_value__attribute__attribute_name__in=['color', 'size'],
            attribute_value__attribute_value__in=[color, size]
        ).first()
        
        print(f"Found product_variant: {product_variant}")

        if product_variant:
            if product_variant.stock >= 1:
                if request.user.is_authenticated:
                    cart, created = Cart.objects.get_or_create(user=request.user)

                    is_cart_item_exists = CartItem.objects.filter(
                        cart=cart,
                        product_variant=product_variant
                    ).exists()

                    if is_cart_item_exists:
                        cart_item = CartItem.objects.get(
                            cart=cart,
                            product_variant=product_variant,
                        )

                        if qyt < product_variant.stock:
                            cart_item.quantity += qyt
                            cart_item.save()
                            messages.success(request, "Item quantity updated.")
                        else:
                            messages.success(request, "Product out of stock")
                    else:
                        CartItem.objects.create(cart=cart, product_variant=product_variant, quantity=qyt)
                        messages.success(request, "Item added to the cart.")
                    return redirect('cart_mng:cart')
                else:
                    messages.success(request, "Please login to purchase")
                    return redirect('log:user_login')
            else:
                messages.warning(request, 'This item is out of stock.')
                return redirect('log:product_detail', id)
        else:
            messages.warning(request, 'Variation not available, please select another variation')
            return redirect('log:product_detail', id)
    except Product.DoesNotExist:
        messages.warning(request, 'Product does not exist')
    except Exception as e:
        print(f"The error is {e}")
        messages.error(request, 'An error occurred, please try again later.')

    return redirect('cart_mng:cart')







def newcart_update(request):
    print('newcart_update view is called')

    new_quantity = 0
    total = 0
    tax = 0
    grand_total = 0
    sub_total = 0
    counter = 0

    if request.method == 'POST' and request.user.is_authenticated:
        print('impliment ajax')
        prod_id = int(request.POST.get('product_id'))
        cart_item_id = int(request.POST.get('cart_id'))
        qyt = int(request.POST.get('qyt'))
        counter = int(request.POST.get('counter'))

        product_variant = get_object_or_404(ProductVariant, id=prod_id)
        cart = Cart.objects.get(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=product_variant)

        if cart_item.product_variant:
            if cart_item.quantity < product_variant.stock:
                cart_item.quantity += 1
                cart_item.save()
                sub_total = cart_item.subtotal()
                new_quantity = cart_item.quantity
            else:
                return JsonResponse({'status': 'error', 'message': 'Stoke limit reached.Cannot add more to cart'})

        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += cart_item.subtotal()

        tax = (2 * total) / 100
        grand_total = total + tax

    if new_quantity == 0:
        message = "Out of stock"
        return JsonResponse({'status': 'error', 'message': message})
    else:
        return JsonResponse({
            'status': "success",
            'new_quantity': new_quantity,
            'total': total,
            'tax': tax,
            'counter': counter,
            'grand_total': grand_total,
            'sub_total': sub_total
        })


def remove_cart_item_fully(request):
    new_quantity = 0
    total = 0
    tax = 0
    grand_total = 0
    counter = 0

    if request.method == 'POST' and request.user.is_authenticated:
        pro_id = int(request.POST.get('product_id'))
        cart_item_id = int(request.POST.get('cart_id'))
        qyt = int(request.POST.get('qyt'))
        counter = int(request.POST.get('counter'))

        product_variant = get_object_or_404(ProductVariant, id=pro_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_variant=product_variant)

        if cart_item.product_variant:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                sub_total = cart_item.subtotal()
                new_quantity = cart_item.quantity

        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += cart_item.subtotal()

        tax = (2 * total) / 100
        grand_total = total + tax

    if new_quantity == 0:
        message = "Sorry, the quantity cannot be less than 1. If you want to remove this item, please use the 'Remove' option instead."
        return JsonResponse({'status': 'error', 'message': message})
    else:
        return JsonResponse({
            'status': "success",
            'new_quantity': new_quantity,
            'total': total,
            'tax': tax,
            'counter': counter,
            'grand_total': grand_total,
            'sub_total' : sub_total,
        })
    




def remove_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(cart__user=request.user, id=cart_item_id)
        cart_item.delete()
        print ('helllo in cart ')
        return JsonResponse({'status': True, 'message': 'Product is deleted successfully'})
    except CartItem.DoesNotExist:
        pass 
    return redirect('cart_mng:cart')
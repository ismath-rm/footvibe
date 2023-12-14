from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, ExpressionWrapper
from django.contrib import messages
from cart_management.models import *
from product_management.models import *
from django.core.exceptions import ObjectDoesNotExist


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        sub_total = 0

        if request.user.is_authenticated:
            # Filter carts with at least one active CartItem
            cart_items = CartItem.objects.filter(cart__user=request.user)
            active_carts = Cart.objects.filter(cartitem__in=cart_items).distinct()

            # Use the active carts to retrieve cart items
            cart_items = CartItem.objects.filter(cart__in=active_carts)

            for cart_item in cart_items:
                total += (cart_item.product_variant.sale_price * cart_item.quantity)
                # sub_total = (cart_item.product_variant.sale_price * cart_item.quantity)
                # print(sub_total,"sub_totalsub_totalsub_totalsub_totalsub_totalsub_total")
                quantity += cart_item.quantity


            tax = (2 * total) / 100
            grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        # 'sub_total':sub_total,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'user/cart.html', context)




def add_cart(request, id):
    color = request.POST.get('color')
    size = request.POST.get('size')
    qyt = request.POST.get('input')
    print(qyt)
    qyt = int(qyt)
    print(f'qyt = {qyt}')
    try:
        id = Product.objects.get(id=id)
        
        product_variant = ProductVariant.objects.filter(
            product=id,
            attribute_value__attribute__attribute_name__in=['color', 'size'],
            attribute_value__attribute_value__in=[color, size]
        ).first()
    
        if product_variant.stock >= 1:
            if request.user.is_authenticated:
                is_cart_item_exists = CartItem.objects.filter(
                    cart__user=request.user,
                    product_variant=product_variant
                ).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.get(
                        cart__user=request.user,
                        product_variant=product_variant,
                    )

                    if qyt < product_variant.stock:
                        cart_item.quantity += qyt
                        cart_item.save()
                        messages.success(request, "Item quantity updated.")
                    else:
                        messages.success(request, "Product out of stock")
                else:
                    cart, created = Cart.objects.get_or_create(user=request.user)
                    CartItem.objects.create(cart=cart, product_variant=product_variant, quantity=1)
                    messages.success(request, "Item added to the cart.")
                    return redirect('cart_mng:cart')
            else:
                messages.success(request, "Please login to purchase")
                return redirect('log:user_login')
        else:
            messages.warning(request, 'This item is out of stock.')
            return redirect('log:product_detail', id)
    except ProductVariant.DoesNotExist:
        messages.warning(request, 'Variation not available, please select another variation')
    except Exception as e:
        print(f"The error is {e}")

    return redirect('cart_mng:cart')



def remove_cart(request, product_id, cart_item_id):
    product_variant = get_object_or_404(ProductVariant, id=product_id)

    try:
        cart_item = CartItem.objects.get(cart__user=request.user, product_variant=product_variant, id=cart_item_id)

        print("Cart Item Product Variant (All):", cart_item.product_variant.all())
        print("Cart Item Product Variant (First):", cart_item.product_variant.first())

        if cart_item.quantity >= 1:
            if cart_item.product_variant:
                print('in the cahnges')
                cart_item.product_variant.stock += 1
                cart_item.quantity -= 1
                cart_item.product_variant.save()
                cart_item.save()
        else:
            cart_item.delete()

    except CartItem.DoesNotExist:
        pass  # Handle the case where the cart item doesn't exist

    return redirect('cart_mng:cart')



def remove_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(cart__user=request.user, id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # Handle the case where the cart item doesn't exist

    return redirect('cart_mng:cart')
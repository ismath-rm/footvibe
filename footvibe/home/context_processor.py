from cart_management.models import Cart,CartItem
from home.models import Account

def menu_link(request):
    cart_count = 0
    try:
        cart = Cart.objects.get(user=request.user)
        cart_count = CartItem.objects.filter(cart_id=cart).count()
    except Exception:
        cart_count = 0
    return {"cart_count": cart_count}
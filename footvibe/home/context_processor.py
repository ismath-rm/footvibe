from cart_management.models import Cart, CartItem
from home.models import *

def menu_link(request):
    cart_count = 0
    wishlist_count = 0  # Initialize wishlist_count before the try block

    try:
        cart = Cart.objects.get(user=request.user)
        cart_count = CartItem.objects.filter(cart_id=cart).count()
        wishlist = Wishlist.objects.get_or_create(user=request.user)[0]
        wishlist_items = WishlistItems.objects.filter(wishlist=wishlist)
        wishlist_count = wishlist_items.count()
    except Exception as e:
        # Handle the exception (you might want to log it for debugging purposes)
        print(f"Error in menu_link: {e}")
        wishlist_count = 0  # Set a default value for wishlist_count

    return {"cart_count": cart_count, "wishlist_count": wishlist_count}


from home.models import Account
from django.db import models
from product_management.models import ProductVariant

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    items = models.ManyToManyField(ProductVariant, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def subtotal(self):
        return self.product_variant.sale_price * self.quantity

    def __str__(self):
        return f"{self.product_variant.get_product_name()} in Cart for {self.cart.user.username}"

from django.db import models
from product_management.models import *
from home.models import *

# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_amount = models.IntegerField(default=1000)
    valid_to = models.DateField()


    def Is_Redeemed_By_User_New(self, request, user):
        coupon_code = request.POST.get("couponCode")
        # Assuming there is a Coupon model with a field named 'coupon_code'
        coupon = Coupon.objects.get(coupon_code=coupon_code)

        print(coupon)
        redeemed_details = Coupon_Redeemed_Details.objects.filter(coupon=coupon, user=user)
        print(redeemed_details, redeemed_details.exists())
        return redeemed_details.exists()
    def __str__(self):
         return self.coupon_code
     

class Coupon_Redeemed_Details(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_redeemed = models.BooleanField(default=False)
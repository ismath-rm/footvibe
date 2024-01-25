# from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from product_management.models import *
from django.core.exceptions import ValidationError
# from django.utils import timezone
# from django.contrib.auth.models import AbstractBaseUser, UserManager,PermissionsMixin,Permission,Group

class AccountManager(BaseUserManager):
    def create_user(self, username, email, phone, password):
        if not email:
            raise ValueError("User must have a email")
        if not username:
            raise ValueError("User must have an username")
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone
            
        )

        # user.is_active = True
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            phone=phone
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom user model
class Account(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone =models.CharField(max_length=50)
   

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", 'phone']

    objects = AccountManager()

    def __str__(self):
        return self.email

    # Check user permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Check user module permissions
    def has_module_perms(self, add_label):
        return True
    

class AddressBook(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True, default=None)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    phone = models.CharField(max_length=15,default=9633018297)
    email = models.EmailField(max_length=100, default='ismathrm(@gmail.com)')
    address_line_1 = models.CharField(max_length=150,null=True,blank=True)
    address_line_2 = models.CharField(max_length=150,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    city =models.CharField(max_length=50,null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.address_line_1
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Set is_default=False for other addresses of the same user
            AddressBook.objects.filter(user=self.user).exclude(
                pk=self.pk).update(is_default=False)
        super(AddressBook, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=16)  # Store the OTP secret key



class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    

    # def __str__(self):
    #     return f"Wishlist for {self.user.username}"
    
    # class Meta:
    #     verbose_name = 'Wishlist'
    #     verbose_name_plural = 'Wishlists'


class WishlistItems(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.product.get_product_name()} in Wishlist for {self.wishlist.user.username}"
    
    # class Meta:
    #     verbose_name = 'Wishlist Item'
    #     verbose_name_plural = 'Wishlist'


class Wallet(models.Model):
    user=models.OneToOneField(Account, on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)
    
class WalletHistory(models.Model):
    wallet=models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type=models.CharField(null=True, blank=True, max_length=20)
    created_at=models.DateField(auto_now_add=True)
    amount=models.IntegerField()



class HomeMainSlide(models.Model):
    heading = models.CharField(max_length = 20, null = False)
    subheading = models.CharField(max_length = 30, null = True)
    slide_image = models.ImageField(upload_to = 'banners')

    def __str__(self):
        return self.heading
    
    # fucntion for validating the inputs of model mainly aspect ration of image
    def clean(self):
        max_width = 1920
        max_height = 1080
        aspect_ratio = max_width/max_height
        total_slides = HomeMainSlide.objects.count()


        if self.slide_image:
            image=Image.open(self.slide_image)
            img_width, img_height = image.size
            img_aspect_ratio = img_width/img_height

            if abs(img_aspect_ratio-aspect_ratio) > 1.2 and abs(img_aspect_ratio-aspect_ratio)< 1.8:
                raise ValidationError(f'The image aspect ratio must be {aspect_ratio}:1')
            
        if total_slides >= 3:
            raise ValidationError("You can only have a maximum of 3 slides in HomeMainSlide.")
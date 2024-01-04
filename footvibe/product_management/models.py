from django.db import models
from django.utils.text import slugify
import uuid
from django.urls import reverse

# Create your models here.
class Category(models.Model):
        category_name = models.CharField(max_length=20, unique=True)
        slug = models.SlugField(max_length=20, blank=True, unique=True)
        description = models.TextField(max_length=200, blank=True)
        parent = models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE)
        is_available = models.BooleanField(default=True)
        
        

        class Meta:
            verbose_name = 'category'
            verbose_name_plural = 'categories'

        def save(self, *args, **kwargs):
            if not self.slug:
                unique_identifier = str(uuid.uuid4())[:8]
                self.slug = f"{slugify(self.category_name)}-{unique_identifier}"
            super(Category, self).save(*args, **kwargs)

        def __str__(self):
            return self.category_name
        


class Brand(models.Model):
        brand_name = models.CharField(max_length=50,unique=True)
        is_active = models.BooleanField(default=True)

        def __str__(self):
            return self.brand_name
        


class Attribute(models.Model):
        attribute_name = models.CharField(max_length=50,unique=True)
        is_active = models.BooleanField(default=True)

        def __str__(self):
            return self.attribute_name
        

class Attribute_Value(models.Model):
        attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)
        attribute_value = models.CharField(max_length=50,unique=True)
        is_active = models.BooleanField(default=True)

        def __str__(self):
            return self.attribute_value+"-"+self.attribute.attribute_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_catg = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    product_brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    product_slug = models.SlugField(unique=True, blank=True,max_length=200)
    product_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    

    def save(self, *args, **kwargs):
        product_slug_name = f'{self.product_brand.brand_name} {self.product_name} {self.product_catg.category_name}'
        base_slug = slugify(product_slug_name)
        counter = Product.objects.filter(product_slug__startswith=base_slug).count()
        if counter > 0:
            self.product_slug = f'{base_slug}-{counter}'
        else:
            self.product_slug = base_slug
        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.product_brand.brand_name+"-"+self.product_name+"-"+self.product_catg.category_name
    
    def get_product_name(self):
        return f'{self.product_brand} {self.product_name} ({self.product_catg.category_name})'



class ProductVariant(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    sku_id = models.CharField(max_length=30)
    attribute_value = models.ManyToManyField(Attribute_Value,related_name='attributes', blank=True)
    max_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    product_variant_slug = models.SlugField(blank=True,max_length=200)
    is_active = models.BooleanField(default=True)
    thumbnail_image = models.ImageField(upload_to='product_variant/images/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = models.Manager()
    
    def __str__(self):
        attribute_values = ', '.join([str(value) for value in self.attribute_value.all()])
        return f"{self.product.product_name} {attribute_values}"

   
    
    
    def save(self, *args, **kwargs):
        
        # Build the slug using the fetched values
        product_variant_slug_name = f'{self.product.product_brand.brand_name}-{self.product.product_name}-{self.product.product_catg.category_name}-{self.sku_id}'
        base_slug = slugify(product_variant_slug_name)
        
        # Count the existing slugs
        counter = ProductVariant.objects.filter(product_variant_slug__startswith=base_slug).exclude(pk=self.pk).count()

        # Append the counter if necessary
        if counter > 0:
            self.product_variant_slug = f'{base_slug}-{counter}'
        else:
            self.product_variant_slug = base_slug

        super(ProductVariant, self).save(*args, **kwargs)
    
     
        
    def get_url(self):
        return reverse('product-variant-detail',args=[self.product.product_catg.slug,self.product_variant_slug])
    
    def get_product_name(self):
        attribute_values = ', '.join([value.attribute_value for value in self.attribute_value.all()])
        return f'{self.product.product_brand} {self.product.product_name}-{self.sku_id} - {attribute_values}'

    
    def get_url(self):
        return reverse('log:product_detail', args=[self.product_variant_slug])


class ProductImage(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='photos/product_variant', null=True)

    def __str__(self):
        return self.image.url        

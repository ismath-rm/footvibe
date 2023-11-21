from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from .models import Category,Brand,Attribute,Attribute_Value,Product
from .forms import CreateProductForm
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here.
#......................................................category..............................................................#
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    categories = Category.objects.all()
    content = {
        'categories': categories
    }
    return render(request, 'admin/category.html',content)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_category(request):
    category_name = request.POST['category_name']
    parent = None if request.POST['parent'] == 'None' else Category.objects.get(category_name=request.POST['parent'])
    description = request.POST['description']

    Category.objects.create(
        category_name=category_name,
        parent=parent,
        description=description,
        
    )
    return redirect('product_mng:category')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def available(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    category = get_object_or_404(Category, id=category_id)
    
    if category.is_available:
        category.is_available=False
       
    else:
        category.is_available=True
    category.save()

    
    cat_list=Category.objects.filter(parent_id=category_id)
  
    
    for category in cat_list:
        if category.is_available:
            category.is_available=False
        else:
            category.is_available=True
        category.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_category(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        category=Category.objects.get(id=category_id)
    except ValueError:
        return redirect('product_mng:category')
    category.delete()

    return redirect('product_mng:category')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_category(request,category_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    category_list=Category.objects.get(id=category_id)
    category_name=category_list.category_name
    category_disc=category_list.description
   
    content={
        'category_name':category_name,
        'category_disc':category_disc
    }
    
    if request.method == "POST":
        cat_name = request.POST['category_name']
        cat_desc = request.POST['description']
        
        category_list.category_name=cat_name
        category_list.description=cat_desc
        category_list.save()

        return redirect('product_mng:category')

    return render(request,'admin/edit_category.html',content)




#...............................................brand...........................................................#



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brands(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    brands = Brand.objects.all()
    content = {
        'brands': brands
    }
    return render(request, 'admin/brands.html',content)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_brand(request):
        brand_name = request.POST['brand_name']
        print("welcome")
        print(brand_name)
        Brand.objects.create(
            brand_name=brand_name,
        )
        return redirect('product_mng:brands')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def brand_available(request,brand_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    brand = get_object_or_404(Brand, id=brand_id)
    
    if brand.is_active:
        brand.is_active=False
       
    else:
        brand.is_active=True
    brand.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_brand(request,brand_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        brand=Brand.objects.get(id=brand_id)
    except ValueError:
        return redirect('product_mng:brands')
    brand.delete()

    return redirect('product_mng:brands')

#...........................................attribute.....................................................#

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    attributes = Attribute.objects.all()
    content = {
        'attributes': attributes
    }
    return render(request, 'admin/attribute.html',content)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_attribute(request):
    attribute_name = request.POST['attribute_name']
    Attribute.objects.create(
        attribute_name=attribute_name,
    )
    return redirect('product_mng:attribute')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_available(request,attribute_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
   
    attribute = Attribute.objects.get(id=attribute_id)
    
    if attribute.is_active:
        attribute.is_active=False
       
    else:
        attribute.is_active=True
    attribute.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_attribute(request,attribute_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        attribute=Attribute.objects.get(id=attribute_id)
    except ValueError:
        return redirect('product_mng:attribute')
    attribute.delete()

    return redirect('product_mng:attribute')

#................................................attribute value.......................................................#

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_value(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    attribute_values = Attribute_Value.objects.all()
    attribute_names=Attribute.objects.all()
    content = {
        'attribute_values': attribute_values,
        'attribute_names': attribute_names
    }
    return render(request,'admin/attribute_value.html',content)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_attribute_value(request):
    if request.method == 'POST':
        attribute_value_n = request.POST.get('attribute_value_name')
        attribute = request.POST.get('attribute')
        print(attribute_value_n)
        print(attribute)
        if attribute_value_n and attribute:
            print("hoiiiiiiiiiiiiiiii")
            attribute_id = Attribute.objects.get(attribute_name=attribute)
            Attribute_Value.objects.create(
                attribute_value=attribute_value_n,
                attribute_id=attribute_id.id
            )
    
    attribute_values = Attribute_Value.objects.all()
    attribute_names = Attribute.objects.all()
    context = {
        'attribute_values': attribute_values,
        'attribute_names': attribute_names
    }
    
    return render(request, 'admin/attribute_value.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_value_available(request,attribute_value_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
   
    attribute_value = Attribute_Value.objects.get(id=attribute_value_id)
    
    if attribute_value.is_active:
        attribute_value.is_active=False
       
    else:
        attribute_value.is_active=True
    attribute_value.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_attribute_value(request,attribute_value_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        attribute_value=Attribute_Value.objects.get(id=attribute_value_id)
    except ValueError:
        return redirect('product_mng:attribute_value')
    attribute_value.delete()

    return redirect('product_mng:attribute_value')


#......................................product...............................................#

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products_list(request):
    product_values = Product.objects.all()
    context = {
        'product_values':product_values
    }

    return render(request,'admin/products_list.html',context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_product(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    categories = Category.objects.all()
    brands = Brand.objects.all().exclude(is_active=False)    

    if request.method == 'POST':
        product_name= request.POST.get('product_name')
        product_sk_id= request.POST.get('sku_id')
        description= request.POST.get('product_desc')
        max_price= request.POST.get('product_max_price')
        sale_price= request.POST.get('product_sale_price')
        category_name= request.POST.get('product_category')
        brand_name=request.POST.get('product_brand')

       
        category = get_object_or_404(Category, category_name=category_name)
        brand = get_object_or_404(Brand, brand_name=brand_name)

        product = Product(
            product_name=product_name,
            sku_id=product_sk_id,
            product_catg=category,
            product_brand=brand,
            product_description=description,
            max_price=max_price,
            sale_price=sale_price,
            image=request.FILES['image_feild']  # Make sure your file input field is named 'product_image'
        )
        product.save()

        return redirect('product_mng:add_product')
    else:
        form=CreateProductForm()
    content = {
        'categories': categories,
        'brands': brands,   
        'form': form
    }
    return render(request,'admin/add_product.html', content)


from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Category,Brand,Attribute,Attribute_Value,Product,ProductVariant, ProductImage
from .forms import CreateProductForm
from django.utils.text import slugify
from django.db import IntegrityError
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .forms import ProductVariantForm 
from django.contrib import messages
import re

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
    return render(request, 'admin_temp/category.html',content)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_category(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        parent_name = request.POST.get('parent')
        description = request.POST.get('description')

        # Basic validation checks
        if not category_name or not description:
            messages.error(request, 'Category name and description are required.')
            return redirect('product_mng:category')
        
        # Validate category name
        if any(re.match('[@#$%^@%@#%&]', char) for char in category_name) or category_name.startswith(" "):
            messages.error(request, "Invalid category name")
            return redirect('product_mng:category')


        # Check if the category already exists
        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, 'Category with this name already exists.')
            return redirect('product_mng:category')

        # Continue with creating the category
        parent = None if parent_name == 'None' else Category.objects.get(category_name=parent_name)
        Category.objects.create(
            category_name=category_name,
            parent=parent,
            description=description,
        )
        messages.success(request, f'Category "{category_name}" has been successfully added.')
        return redirect('product_mng:category')





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def available(request,category_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
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
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    try:
        category=Category.objects.get(id=category_id)
    except ValueError:
        return redirect('product_mng:category')
    category.delete()

    return redirect('product_mng:category')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_category(request,category_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    category_list=Category.objects.get(id=category_id)
    category_name=category_list.category_name
    category_disc=category_list.description
   
    content={
        'category_list': category_list,
        'category_name':category_name,
        'category_disc':category_disc,
    }
    
    if request.method == "POST":
        cat_name = request.POST['category_name']
        cat_desc = request.POST['description']


        if not cat_name or not cat_name.strip() or any(re.match('[@#$%^@%@#%&]', char) for char in cat_name):
            messages.error(request, 'Invalid category name')
            return render(request, 'admin_temp/edit_category.html', content)

        

        new_slug = slugify(cat_name)
        if Category.objects.filter(slug=new_slug).exclude(id=category_list.id).exists():
            messages.error(request, 'Category with this name already exists. Please choose a different name.')
            return render(request, 'admin_temp/edit_category.html', content)


        category_list.category_name=cat_name
        category_list.slug = new_slug  
        category_list.description=cat_desc
        category_list.save()

        messages.success(request, 'Category updated successfully')
        return redirect('product_mng:category')

    return render(request,'admin_temp/edit_category.html',content)




#...............................................brand...........................................................#



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brands(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    brands = Brand.objects.all()
    content = {
        'brands': brands
    }
    return render(request, 'admin_temp/brands.html',content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_brand(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    brand_name = request.POST.get('brand_name', '')  # Use get() to handle the case when 'brand_name' is not in POST
    
    print(f"Brand name received: {brand_name}")

    # Validate brand name
    if not brand_name or any(re.match('[@#$%^@%@#%&]', char) for char in brand_name) or brand_name.startswith(" "):
        messages.error(request, "Invalid brand name")
        return redirect('product_mng:brands')
    
    if Brand.objects.filter(brand_name=brand_name).exists():
        messages.warning(request, f"Brand '{brand_name}' already exists.")
        return redirect('product_mng:brands')
    
    try:

        Brand.objects.create(
            brand_name=brand_name,
        )

        messages.success(request, f"Brand '{brand_name}' created successfully!")

    except IntegrityError as e:

        messages.error(request, f"Failed to create brand '{brand_name}'. Please try again.")


    return redirect('product_mng:brands')







@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def brand_available(request,brand_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    brand = get_object_or_404(Brand, id=brand_id)
    
    if brand.is_active:
        brand.is_active=False
       
    else:
        brand.is_active=True
    brand.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_brand(request,brand_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    try:
        brand=Brand.objects.get(id=brand_id)
    except ValueError:
        return redirect('product_mng:brands')
    brand.delete()

    return redirect('product_mng:brands')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_brand(request, brand_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    brand = get_object_or_404(Brand, id=brand_id)
    
    if request.method == "POST":
        brand_name = request.POST['brand_name']

        if not brand_name or any(re.match('[@#$%^@%@#%&]', char) for char in brand_name) or brand_name.startswith(" "):
            messages.error(request, "Invalid brand name")
            return redirect('product_mng:edit_brand', brand_id=brand_id)


        try:
            brand.brand_name = brand_name
            brand.save()

            messages.success(request, f"Brand '{brand_name}' updated successfully!")
            return redirect('product_mng:brands')
        
        except IntegrityError:
            messages.error(request, f"Brand '{brand_name}' already exists. Choose a different name.")
            return redirect('product_mng:edit_brand', brand_id=brand_id)

    content = {
        'brand_id': brand.id,
        'brand_name': brand.brand_name,
    }

    return render(request, 'admin_temp/edit_brand.html', content)


#...........................................attribute.....................................................#

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    attributes = Attribute.objects.all()
    content = {
        'attributes': attributes
    }
    return render(request, 'admin_temp/attribute.html',content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_attribute(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')

    attribute_name = request.POST['attribute_name']
    
    # Validate attribute name
    if not attribute_name or any(re.match('[@#$%^@%@#%&]', char) for char in attribute_name) or attribute_name.startswith(" "):
        messages.error(request, "Invalid attribute name")
        return redirect('product_mng:attribute')

    try:
        # Check if the attribute already exists
        existing_attribute = Attribute.objects.filter(attribute_name=attribute_name).first()

        if existing_attribute:
            messages.warning(request, f"Attribute '{attribute_name}' already exists.")
        else:
            # Create the Attribute object if it doesn't exist
            Attribute.objects.create(attribute_name=attribute_name)
            messages.success(request, "Attribute added successfully.")

    except Exception as e:
        messages.error(request, f"Failed to add attribute. Error: {str(e)}")

    return redirect('product_mng:attribute')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_available(request,attribute_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
   
    attribute = Attribute.objects.get(id=attribute_id)
    
    if attribute.is_active:
        attribute.is_active=False
       
    else:
        attribute.is_active=True
    attribute.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_attribute(request,attribute_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    try:
        attribute=Attribute.objects.get(id=attribute_id)
    except ValueError:
        return redirect('product_mng:attribute')
    attribute.delete()

    return redirect('product_mng:attribute')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_attribute(request, attribute_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    attribute = get_object_or_404(Attribute, id=attribute_id)
    
    if request.method == "POST":
        attribute_name = request.POST['attribute_name']

        if not attribute_name or any(re.match('[@#$%^@%@#%&]', char) for char in attribute_name) or attribute_name.startswith(" "):
            messages.error(request, "Invalid attribute name")
            return redirect('product_mng:edit_attribute', attribute_id=attribute_id)


        try:

            attribute.attribute_name = attribute_name
            attribute.save()
            messages.success(request, f"Attribute '{attribute_name}' updated successfully!")
            return redirect('product_mng:attribute')
        
        except IntegrityError:
            messages.error(request, f"Attribute '{attribute_name}' already exists. Choose a different name.")
            return redirect('product_mng:edit_attribute', attribute_id=attribute_id)


    content = {
        'attribute': attribute,
    }

    return render(request, 'admin_temp/edit_attribute.html', content)

#................................................attribute value.......................................................#

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_value(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    attribute_values = Attribute_Value.objects.all()
    attribute_names  = Attribute.objects.all()
    content = {
        'attribute_values': attribute_values,
        'attribute_names': attribute_names
    }
    return render(request,'admin_temp/attribute_value.html',content)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_attribute_value(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')

    if request.method == 'POST':
        attribute_value_n = request.POST.get('attribute_value_name')
        attribute = request.POST.get('attribute')

        if not attribute_value_n or not attribute:
            messages.error(request, "Please provide both attribute name and value.")
            return redirect('product_mng:attribute_value')

        # Validate the attribute_value_n using a regex pattern
        if not re.match(r'^[\w.@+-]+$', attribute_value_n):
            messages.error(request, "Invalid attribute value name. Please use only letters,")
            return redirect('product_mng:attribute_value')

        try:
            attribute_obj = Attribute.objects.get(attribute_name=attribute)

            # Check if the attribute value already exists for the selected attribute
            existing_attribute_value = Attribute_Value.objects.filter(
                attribute_value=attribute_value_n,
                attribute_id=attribute_obj.id
            ).first()

            if existing_attribute_value:
                messages.warning(request, f"Attribute value '{attribute_value_n}' already exists for the selected attribute.")
            else:
                # Create the Attribute_Value object if it doesn't exist
                Attribute_Value.objects.create(
                    attribute_value=attribute_value_n,
                    attribute_id=attribute_obj.id
                )
                messages.success(request, "Attribute value added successfully.")

        except Attribute.DoesNotExist:
            messages.error(request, f"Invalid attribute name: {attribute}")
            return redirect('product_mng:attribute_value')

    attribute_values = Attribute_Value.objects.all()
    attribute_names = Attribute.objects.all()
    context = {
        'attribute_values': attribute_values,
        'attribute_names': attribute_names
    }

    return render(request, 'admin_temp/attribute_value.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attribute_value_available(request,attribute_value_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    attribute_value = Attribute_Value.objects.get(id=attribute_value_id)
    
    if attribute_value.is_active:
        attribute_value.is_active=False
       
    else:
        attribute_value.is_active=True
    attribute_value.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_attribute_value(request,attribute_value_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    try:
        attribute_value=Attribute_Value.objects.get(id=attribute_value_id)
    except ValueError:
        return redirect('product_mng:attribute_value')
    attribute_value.delete()

    return redirect('product_mng:attribute_value')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_attribute_value(request, attribute_value_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    attribute_value = get_object_or_404(Attribute_Value, id=attribute_value_id)
    
    if request.method == "POST":
        attribute_value_name = request.POST['attribute_value_name']
        attribute_name = request.POST['attribute']

        attribute = Attribute.objects.get(attribute_name=attribute_name)

        if not attribute_value_name or not attribute_value_name.strip():
            messages.error(request, "Invalid attribute value name")
            return redirect('product_mng:edit_attribute_value', attribute_value_id=attribute_value_id)


        try:
            attribute_value.attribute_value = attribute_value_name
            attribute_value.attribute_id = attribute.id
            attribute_value.save()

            messages.success(request, f"Attribute value '{attribute_value_name}' updated successfully!")
            return redirect('product_mng:attribute_value')
        
        except IntegrityError:
            messages.error(request, f"Attribute value '{attribute_value_name}' already exists. Choose a different name.")
            return redirect('product_mng:edit_attribute_value', attribute_value_id=attribute_value_id)


    content = {
        'attribute_value': attribute_value,
        'attribute_names': Attribute.objects.all(),
    }

    return render(request, 'admin_temp/edit_attribute_value.html', content)




#.......................................................product.............................................................#




@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def products_list(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')

    product_values = Product.objects.all().order_by('-created_at')
    
    # for product in product_values:
    #     total_stock = sum([variant.stock for variant in product.productvariant_set.all()])
    #     product.total_stock = total_stock


    context = {
        'product_values':product_values
    }

    return render(request,'admin_temp/products_list.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_product(request):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    

    categories = Category.objects.all()
    brands = Brand.objects.all().exclude(is_active=False)  


    if request.method == 'POST':
        product_name= request.POST.get('product_name')
        description= request.POST.get('product_desc')
        category_name= request.POST.get('product_category')
        brand_name=request.POST.get('product_brand')


        # Basic validation checks
        if not product_name or not description or not category_name or not brand_name:
            messages.error(request, "All fields are required")
            return redirect('product_mng:add_product')

        # Product name validation
        if any(re.match('[@#$%^@%@#%&]', char) for char in product_name) or product_name.startswith(" "):
            messages.error(request, "Invalid product name")
            return redirect('product_mng:add_product')

       
        category = get_object_or_404(Category, category_name=category_name)
        brand = get_object_or_404(Brand, brand_name=brand_name)

        product = Product(
            product_name=product_name,
            product_catg=category,
            product_brand=brand,
            product_description=description,
        )
        product.save()

        messages.success(request, "Product added successfully add variants also!") 
        return redirect('product_mng:products_list')
    else:
        form=CreateProductForm()

        
    content = {
        'categories': categories,
        'brands': brands,   
        'form': form
    }
    return render(request,'admin_temp/add_product.html', content)






def variant_list(request, product_id):
    try:
        product = Product.objects.get(id = product_id)
    except Exception as e:
        print(e)
    variants = ProductVariant.objects.filter(product = product).order_by('-is_active')
    success_message = request.GET.get('message', None)

    context = {
        'variants': variants,
        'product': product,
        'success_message': success_message, 
    }
    return render(request, 'admin_temp/product_control/variant_list.html', context)



def product_variant_control(request, product_variant_id):
    try:
        product_variant = ProductVariant.objects.get(id = product_variant_id)
    except Exception as e:
        print(e)


    product_variant.is_active = not product_variant.is_active
    print("hiiiiiiiiiiiiii")
    product_variant.save()
    print("h112345678")
    return redirect('product_mng:variant_list', product_variant.product.id )



def add_product_variant(request, product_id = None):
    if product_id:
        product = Product.objects.filter(id = product_id).first()
    else:
        product = None

    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    
    attributes = Attribute.objects.prefetch_related('attribute_value_set')
    print("=====================================================================================")
    print(attributes)
    attribute_values_count = attributes.count()
    attribute_dict = {}
    for attribute in attributes:
        attribute_values = attribute.attribute_value_set.filter(is_active = True)
        attribute_dict[attribute.attribute_name] = attribute_values
    print(attribute_dict.items(),"llllllllllllllllllllllllllllllllll")

    attribute_values = Attribute_Value.objects.all()
  

    if request.method == 'POST':
        if not product_id:
            product_id= int(request.POST.get('product'))
            product = Product.objects.filter(id = product_id).first()
    
        sku_id= request.POST.get('sku_id')
        attribute_value= request.POST.get('attribute_value')
        print(attribute_value)
        max_price=request.POST.get('max_price')
        sale_price=request.POST.get('sale_price')
        stock=request.POST.get('stock')
        image=request.FILES.get('thumbnail_image')
        additional_images=request.FILES.getlist('additional_images')
        print("the additional image is      -----------------------------", additional_images)

        attribute_ids = []

        for i in range(1,attribute_values_count+1):
            attribute_value_id = request.POST.get('attributes_'+str(i))
            if attribute_value_id != 'None':
                attribute_ids.append(int(attribute_value_id))


        print("hello stephan")

        product_variant = ProductVariant(
            product = product,
            sku_id = sku_id,
            max_price = max_price,
            sale_price = sale_price,
            stock = stock,
            thumbnail_image = image
        )
        product_variant.save()
        image_objects = []

        for image in additional_images:
            variant_image = ProductImage.objects.create(product_variant = product_variant, image = image)
            variant_image.save()

        product_variant.attribute_value.set(attribute_ids)

        product_variant.save()
        messages.success(request, 'Variant created successfully !!! ')
        return redirect('product_mng:products_list')
    else:
        form=ProductVariantForm()
    
    
    context = {
        'product': product,
        'attribute_value':attribute_values,
        'attribute_dict':attribute_dict,
        'form': form,

    }

    return render(request, 'admin_temp/add_product_variant.html', context)



def edit_product_variant(request, product_variant_slug):
    try:
        product_variant = ProductVariant.objects.get(product_variant_slug=product_variant_slug)
    except ProductVariant.DoesNotExist:
        messages.error(request, "Product variant not found.")
        return redirect('product_mng:variant_list', product_variant.product.id)

    current_additional_images = product_variant.product_images.all()

    
    attributes = Attribute.objects.prefetch_related('attribute_value_set')
    attribute_dict = {attribute.attribute_name: attribute.attribute_value_set.filter(is_active=True) for attribute in attributes}

    selected_attribute_values = None
    print(product_variant)
    if request.method == 'POST':
        form = ProductVariantForm(request.POST,request.FILES, instance=product_variant)
        if form.is_valid():
            form.instance.product_id = request.POST.get('product')
            form.save()

            multi_image = request.FILES.getlist('additional_images')
            for image in multi_image:
                variant_image = ProductImage.objects.create(product_variant=product_variant,image=image)
                variant_image.save()

            messages.success(request, "Variant Updated")

            return redirect('product_mng:variant_list', product_id=product_variant.product.id)
        else:
            

            messages.error(request, form.errors)

    else:
        form = ProductVariantForm(instance=product_variant)
        selected_attribute_values = product_variant.attribute_value.all().values_list('id', flat=True)
    
    # Check if remove_thumbnail is present in request.POST

    context = {
        'product_variant': product_variant.product,
        'form': form,
        'product_variant_slug': product_variant_slug,
        'product_variant': product_variant,
        'current_additional_images': current_additional_images,
        'attribute_dict': attribute_dict,
        'selected_attribute_values': selected_attribute_values,
    }

    return render(request, 'admin_temp/product_control/edit_product_variant.html', context)

def delete_product_variant_images(request,id,product_variant_slug):
    variant_image = ProductImage.objects.get(id=id)
    variant_image.delete()
    print(product_variant_slug)
    product_variant = ProductVariant.objects.get(product_variant_slug=product_variant_slug)
    messages.success(request, "Variant Updated")
    product_variant_slug = ProductVariant.objects.get(product_variant_slug=product_variant_slug)
    return redirect('product_mng:product_variant_update', product_variant_slug=product_variant.product_variant_slug)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_product(request, product_id):
    if not request.user.is_superuser:
        return redirect('admin_log:admin_login')
    

    
    product = Product.objects.get(id=product_id)
 
    categories = Category.objects.all()
    brands = Brand.objects.all().exclude(is_active=False)

    if request.method == 'POST':
        # product.product_name = request.POST.get('product_name')
        # product.product_description = request.POST.get('description')
        # product.product_catg = request.POST.get('product_catg')
        # product.product_brand = request.POST.get('product_brand')

        
        form = CreateProductForm(request.POST, instance=product)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_mng:products_list')

    else:
        form = CreateProductForm(instance=product)

    context = {
        'categories':categories,
        'brands':brands,
        'form': form,
        'product': product,
    }

    return render(request, 'admin_temp/edit_product.html', context)





def product_control(request, product_id):
    try:
        product = Product.objects.get(id = product_id)
    except Exception as e:
        print(e)


    product.is_active = not product.is_active
    product.save()
    return redirect('product_mng:products_list')




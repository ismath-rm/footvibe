from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from home.models import Account
from django.contrib.auth import login,logout,authenticate
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here. 

def superadmin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Invalid admin credentials!")
            return redirect('admin_log:admin_login')
    return _wrapped_view


@login_required(login_url='admin_log:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@superadmin_required
def dashboard(request):

    return render(request,'admin_temp/index.html')   


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    print("hiii")
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_log:dashboard')

    
    if request.method == 'POST':
        user_email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=user_email, password=password)
        print("helloooooooooo")

        if user:
            if user.is_superuser:
                login(request, user)
                messages.success(request, 'You are logged in successfully')
                return redirect('admin_log:dashboard')
        
        else:
            messages.error(request, 'Login failed. Please check your email and password.')


    return render(request,'admin_temp/admin_login.html')



@login_required(login_url='admin_log:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):

    logout(request)

    return redirect('admin_log:admin_login')


@login_required(login_url='admin_log:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_list(request):

    return render(request,'admin_temp/order_list.html')


@login_required(login_url='admin_log:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_log:admin_login')
    
    search_query=request.GET.get('query')

    if search_query:
         users = Account.objects.filter(username__icontains=search_query)
    else:
         users = Account.objects.all()
         print("the users are :", users)
    context = {
        'users': users
    }
      
    return render(request,'admin_temp/user_list.html',context)


@login_required(login_url='admin_log:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_unblock_user(request,user_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    user = get_object_or_404(Account, id=user_id)
    
    if user.is_active:
        user.is_active=False
        
    else:
        user.is_active=True
        
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
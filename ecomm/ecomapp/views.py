from django.shortcuts import render,redirect,HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from ecomapp.models import *
from django.db.models import Q
import random
import razorpay


# Create your views here.
def home(request):
    context={}
    userid=request.user.id
    # print('id of logged in user:',userid)
    # print('value is:',request.user.is_authenticated)
    p=Product.objects.filter(is_active=True)
    context['data']=p
    cat=Category.objects.all()
    context['cat']=cat
    return render(request,'index.html',context)


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def product_details(request,rid):
    context={}
    #prod_detail=Product.objects.filter(id=rid)
    prod_detail=Product.objects.get(id=rid)
    print('getting',prod_detail)
    context['data']=prod_detail
    return render(request,'product_details.html',context)

def prod_search(request):
    context={}
    srch=request.GET['search']
    if srch:
        c1=Q(name__icontains=srch)
        c2=Q(description__icontains=srch)
        p=Product.objects.filter(c1 | c2)

    else:
        p=Product.objects.none()
    cat=Category.objects.all()
    context['cat']=cat
    context['data']=p
    return render(request,'index.html',context)

def prod_filter(request,rid):
    context={}
    c1=Q(is_active=True)
    c2=Q(category=rid)
    product=Product.objects.filter(c1 & c2)
    cat=Category.objects.all()
    context['data']=product
    context['cat']=cat
    return render(request,'index.html',context)

def sort(request,rid):
    #print(type(rid))
    context={}
    if rid=='0':
        col='price'
    else:
        col='-price'
    cat=Category.objects.all()
    p=Product.objects.filter(is_active=True).order_by(col)
    context['cat']=cat
    context['data']=p
    return render(request,'index.html',context)
    
def range(request):
    context={}
    min = request.GET.get('min', '')  # Get 'min' parameter or default to empty string
    max = request.GET.get('max', '')  # Get 'max' parameter or default to empty string

    if not min or not max:
        context['errormsg']='Fields cannot be Empty'
    elif not min.isdigit() or not max.isdigit():
        context['erormsg']='please enter valid number'
    c1=Q(price__gte=min)
    c2=Q(price__lte=max)
    c3=Q(is_active=True)
    cat=Category.objects.all()
    p=Product.objects.filter(c1 & c2 & c3)
    context['data']=p
    context['cat']=cat
    return render(request,'index.html',context)
 
@login_required(login_url='/login')
def addtocart(request,pid):
    context={}
    u=User.objects.get(id=request.user.id)
    p=Product.objects.get(id=pid)
    print('product is',p)
    cart , created = Cart.objects.get_or_create(uid=u,pid=p)
    if not created:
        context['msg']='product already exist in cart'
    else:
        context['success']='Product added to cart successfully'
    context['data']=p
    return render(request,'product_details.html',context)
     
    
    
    
    
# def addtocart(request,pid):
#     context={}
#     #u=User.objects.filter(id=userid)#u and p are object that we are inserting in cart
#     #print('filter',u)#filter <QuerySet [<User: samantkedar9@gmail.com>]>
#     u=User.objects.filter(id=request.user.id)
#     #print('get',u1)#get samantkedar9@gmail.com
#     #p=Product.objects.filter(id=pid)#u and p are object that we are inserting in cart
#     #print('filter',p)#filter <QuerySet [<Product: Product object (7)>]>
#     p=Product.objects.filter(id=pid)
#     #print('get',p1)#get Product object (7)
    
#     #Check user exist or not
#     c1=Q(uid=u[0])
#     c2=Q(pid=p[0])
#     cart=Cart.objects.filter(c1 & c2)
#     n=len(cart)
#     context['data']=p
#     if n==1:
#         context['msg']='Product already exist in cart!!'
#     # print(userid,pid)  
#     else:
#         cart=Cart.objects.create(uid=u[0],pid=p[0])
#         cart.save()#product added in cart
#         context['success']='product added to cart successfully!!'
    
#     return render(request,'product_details.html',context)


@login_required(login_url='/login')
def viewcart(request):
    print('kedar')
    context={}
    c=Cart.objects.filter(uid=request.user.id)
    sum=0
    for i in c:
        sum = sum + (i.pid.price*i.qty)
        #print(sum)
    context['data']=c
    context['total']=sum
    context['n']=len(c)
    #print('object is',c)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    cart=Cart.objects.filter(id=cid)    
    qty=cart[0].qty
    #print(qty)
    if x=='1':
        qty+=1
    elif qty>1:
        qty-=1
    cart.update(qty=qty)
    return redirect('/viewcart')

def removecart(request,rid):
    cart=Cart.objects.filter(id=rid)
    cart.delete()
    return redirect('/viewcart')
    rder
# def placeorder(request):
#     context={}
#     c=Cart.objects.filter(uid=request.user.id)
#     print('cart is',c)
#     oid=random.randrange(1000,9999)
#     #print('object is',c)
#     for i in c:
#         o=Order.objects.create(order_id=oid,uid=i.uid,pid=i.pid,qty=i.qty)
#         o.save()
#         i.delete()
#     orders=Order.objects.filter(uid=request.user.id)
#     sum=0
#     for i in orders:
#         sum = sum + (i.pid.price*i.qty)
#         #print(sum)
#     context['total']=sum
#     context['n']=len(orders)
#     context['data']=orders
#     return render(request,'place_order.html',context)

import uuid  # For generating unique order IDs

def placeorder(request):
    context = {}
    user_cart = Cart.objects.filter(uid=request.user.id)
    order_id = str(uuid.uuid4())  # Generate a unique order ID

    # Create orders for each item in the cart
    for cart_item in user_cart:
        Order.objects.create(
            order_id=order_id,
            uid=cart_item.uid,
            pid=cart_item.pid,
            qty=cart_item.qty
        )
        cart_item.delete()  # Remove the item from the cart after placing the order

    # Store the current order ID in the session
    request.session['current_order_id'] = order_id

    # Fetch only the orders that were just created (for the current order ID)
    current_orders = Order.objects.filter(order_id=order_id)
    total_amount = sum(order.pid.price * order.qty for order in current_orders)

    # Prepare context for the template
    context['total'] = total_amount
    context['n'] = current_orders.count()
    context['data'] = current_orders

    return render(request, 'place_order.html', context)


from django.conf import settings
def makepayment(request):
    # Fetch the current order ID from the session
    order_id = request.session.get('current_order_id')
    
    if not order_id:
        return HttpResponse("No active order found", status=404)
    
    # Fetch all items in the current order
    current_order_items = Order.objects.filter(order_id=order_id)
    
    if not current_order_items.exists():
        return HttpResponse("No items found in the order", status=404)
    
    # Calculate the total amount for the current order
    total_amount = sum(item.pid.price * item.qty for item in current_order_items)
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create payment data
    data = {
        "amount": int(total_amount * 100),  # Amount in paise
        "currency": "INR",
        "receipt": order_id
    }
    
    # Create Razorpay order
    payment = client.order.create(data=data)
    
    # Prepare context for the template
    context = {
        'data': payment,
        'total_amount': total_amount,
        'order_id': order_id
    }
    
    return render(request, 'pay.html', context)


def order(request):
    order=Order.objects.filter(uid=request.user.id)
    total_amount=sum(item.pid.price*item.qty for item in order)
    n=len(order)
    context={}
    context['total']=total_amount
    context['data']=order
    context['n']=n
    return render(request,'order.html',context)


def register(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=='' or upass=='' or ucpass=='':
            context['errormsg']='Fields cannot be Empty'
            return render(request,'register.html',context)
        elif uname.isnumeric():
            context['errormsg']='Username cannot be numeric'
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errormsg']="Password and Confirm Password did'nt match"
            return render(request,'register.html',context)
        try:
            validate_email(uname)
        except ValidationError:
            context['errormsg'] = 'Invalid email address'
            return render(request, 'register.html', context)
            
        try:
            u=User.objects.create(username=uname,email=uname)
            u.set_password(upass)#it insert a password in database in hash or encrypted format
            u.save()
            context['success']='User created successfully,please login'
            return render(request,'register.html',context)
        except Exception:
            context['errormsg']='User with same Username already exist!'
            return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    

def user_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        
        if uname=='' or upass=='':
            context['errormsg']='Fields cannot be Empty'
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)#it returns the row or object if user is present in auth_user table
            #print( 'u is:',u)
            if u is not None:
                login(request,u)#starts session and stores id of loged in user in session
                return redirect('/')
            else:
                context['errormsg']='Invalid Username or Password!!'
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')
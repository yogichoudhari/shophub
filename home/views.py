from django.shortcuts import render ,redirect
from .models import Product,Cart,Address,PlacedOrder,Customer
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.core import serializers
from django.http import JsonResponse
from django.contrib import auth
from django.conf import settings
from django.core.mail import send_mail
from .forms import (SignupForm , MyPasswordChangeForm ,CustomSetPasswordForm 
,CustomPasswordResetForm,AddressForm)
import re
from django.contrib.auth.views import (PasswordChangeView,PasswordResetView,
PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView)
from django.forms.models import model_to_dict
def home(request):
    return render(request,'home.html')

def product_desc(request,id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request,'product_desc.html',context)

def add_to_cart(request,id=None):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(pk=id)
        Cart(user=user,product=product).save()
        return redirect('/all_product')
    else:
        return redirect('/login')

def cart_plus(request):
    if request.method=="GET":
        id = request.GET['id']
        product = Cart.objects.get(Q(product=id) & Q(user=request.user))
        product.quantity+=1
        product.save()
        products = [p for p in Cart.objects.all() if request.user==p.user]
        quantity = product.quantity
        total_amount = 0
        selling_price = 0
        discounted_price = 0
        amount = 0
        shipping = 40
        for p in products:
            amount += p.quantity*p.product.discounted_price
            selling_price+=p.quantity*p.product.actual_price
        total_amount=amount+shipping
        saved = selling_price - amount
        discounted_price = selling_price-saved
        data = {
            'total_amount':total_amount,
            'amount':amount,
            'saved':saved,
            'discounted_price':discounted_price,
            'selling_price':selling_price,
            'quantity' : quantity
            }
        return JsonResponse(data)
        

def cart_minus(request):
    if request.method=="GET":
        id = request.GET.get('id')
        product = Cart.objects.get(Q(product=id)  & Q(user=request.user))
        product.quantity-=1
        product.save()
        products = [p for p in Cart.objects.all() if request.user==p.user]
        quantity = product.quantity
        total_amount = 0
        selling_price = 0
        discounted_price = 0
        amount = 0
        shipping = 40
        for p in products:
            amount += p.quantity*p.product.discounted_price
            selling_price+=p.quantity*p.product.actual_price
        total_amount=amount+shipping
        saved = selling_price - amount
        discounted_price = selling_price-saved
        data = {
            'total_amount':total_amount,
            'amount':amount,
            'saved':saved,
            'discounted_price':discounted_price,
            'selling_price':selling_price,
            'quantity' : quantity
            }
        return JsonResponse(data)
        
def remove_product(request):
    if request.method=='GET':
        id =request.GET.get('id')
        product = Cart.objects.get(id=id).delete()
        products = [p for p in Cart.objects.all() if request.user==p.user]
        total_amount = 0
        selling_price = 0
        discounted_price = 0
        amount = 0
        shipping = 40
        for p in products:
            amount += p.quantity*p.product.discounted_price
            selling_price+=p.quantity*p.product.actual_price
        total_amount=amount+shipping
        saved = selling_price - amount
        discounted_price = selling_price-saved
        data = {
            'total_amount':total_amount,
            'amount':amount,
            'saved':saved,
            'discounted_price':discounted_price,
            'selling_price':selling_price,
            }
        return JsonResponse(data)      
        
def checkout(request):
    user = request.user
    address_id = request.GET['address']
    address = Address.objects.get(id=address_id)
    print(address)
    cart_products = Cart.objects.filter(user=user)
    for product in cart_products:
        PlacedOrder(user=user,address=address,product=product.product,quantity=product.quantity).save()
        product.delete()
    placed_order = PlacedOrder.objects.filter(user=user) 
    context = {'placed_order':placed_order}
    return render(request,'checkout.html',context)
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        address = Address.objects.filter(user=user)
        cart_products = [p for p in Cart.objects.all() if request.user==p.user]
        total_amount = 0
        selling_price = 0
        discounted_price = 0
        amount = 0
        shipping = 40
        for p in cart_products:
            amount += p.quantity*p.product.discounted_price
            selling_price+=p.quantity*p.product.actual_price
        total_amount=amount+shipping
        saved = selling_price - amount
        discounted_price = selling_price-saved
        context = {'cart':cart,
                   'total_amount':total_amount,
                   'amount':amount,'saved':saved,
                   'discounted_price':discounted_price,
                   'selling_price':selling_price,
                   'address':address
                   }
        return render(request,'cart.html',context)
    else:
        return render(request,'cart.html')
def orders(request):
    return render(request,'orders.html')

def addresses(request):
    form = AddressForm()
    context = {'form':form}
    if request.method=='POST':
        user_id = request.POST['id']
        form = AddressForm(request.POST)
        if form.is_valid():
            form_instance= form.save(commit=False)
            user_obj = User.objects.get(id=user_id)
            form_instance.user = user_obj
            form_instance.save()
            return redirect('/profile')
            
    return render(request,'addresses.html',context)

def all_product(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'all_product.html',context)

def search_item(request):
    search_text = request.GET['search_item']
    women = ['girls','girl','women','Women','lady','ladies']
    women = ''.join(women)
    if search_text in women:
        products = Product.objects.filter(gender_category='Women')
        context = {'products':products}
        return render(request,'all_product.html',context)
    products = Product.objects.filter(Q(title__icontains=search_text) | Q(gender_category__icontains=search_text))
    context = {'products':products}
    return render(request,'all_product.html',context)

def mens_wear(request):
    products = Product.objects.filter(gender_category='Men')
    context = {'products':products}
    return render(request,'all_product.html',context)
def womens_wear(request):
    products = Product.objects.filter(gender_category='Women')
    context = {'products':products}
    return render(request,'all_product.html',context)
def mobile(request):
    products = Product.objects.filter(category='M')
    context = {'products':products}
    return render(request,'all_product.html',context)
def home_appliances(request):
    products = Product.objects.filter(category='HA')
    context = {'products':products}
    return render(request,'all_product.html',context)


#Account Related Function Based Views and Class Based Views starts from here

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    form_class = MyPasswordChangeForm
    success_url = '/password_success'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    form_class = CustomPasswordResetForm
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name='password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='password_reset_confirm.html'
    form_class = CustomSetPasswordForm

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name='password_reset_complete.html'
    
    
def password_success(request):
    return render(request,'password_success.html')

def profile(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    addresses = Address.objects.filter(user=user)
    context = {'addresses':addresses,'customer':customer}
    return render(request,'profile.html',context)

def signup(request):
    if request.user.is_authenticated is False:  
        if request.method=='POST':
                username = request.POST.get('username')
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                if User.objects.filter(email=email).exists():
                    messages.info(request,'Email Is Already Registered')
                    return redirect('/signup')
                if '@gmail.com' not in email:
                    messages.info(request,'Email should be of gmail domain')
                    return redirect('/signup')
                try :
                    phone = int(phone)
                    if len(str(phone))!=10:
                        messages.info(request,'Please Enter Valid Mobile Number')
                        return redirect('/signup')    
                except ValueError as e:
                    messages.info(request,'Please Enter Valid Mobile Number')
                    return redirect('/signup') 
             
                if password1!=password2:
                    messages.info(request,'Password did not match')
                    return redirect('/signup')
                reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
                pattern = re.compile(reg)
                match = re.search(pattern, password1)
                if not match:
                    messages.info(request,'Password should be 6-20 charchters and alphanumeric')
                    return redirect('/signup')
                    
        
                user_obj = User.objects.create_user(username=username,email=email,password=password1)
                auth_token = str(uuid.uuid4())
                customer_obj = Customer(user=user_obj,auth_token=auth_token,phone=phone)
                customer_obj.save()
                send_email_verification(email,auth_token)
                messages.info(request,'Verification email has been sent to you')
                return redirect('/signup')
          
   
        return render(request,'signup_form.html',)
def verify(request,token):
    user_obj = Customer.objects.filter(auth_token=token).first()
    print(user_obj)
    if user_obj:
        user_obj.is_verified = True
        user_obj.save()
        print(user_obj)
        messages.info(request,'Your Email Is Verified Please Login')
        return redirect('/login')
    else:
        messages.info(request,'Invalid Email Address')
        return redirect('/signup')
def send_email_verification(email,auth_token):
    subject = 'Your Account Needs To Be Verified'
    message = f'Hie User Please Click To The Link Verify Your Account https://myshophub.herokuapp.com//verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    
def login(request):
    if request.user.is_authenticated is False:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            print(user_obj)
            if user_obj is None:
                messages.info(request,'User Not Found')
                return redirect('/login')
            customer_obj = Customer.objects.filter(user=user_obj).first()
            print(customer_obj)
            print(customer_obj.is_verified)
            if customer_obj.is_verified:
                user = auth.authenticate(username=username,password=password)
                print(user)
                if user is not None:
                    auth.login(request,user)
                    return redirect('/')
                else:
                    messages.info(request,'Please Enter Correct Password')
                    return redirect('/login')
            
        return render(request,'login.html')

def user_logout(request):
    if request.user.is_authenticated is True:
        auth.logout(request)
        return redirect('/')
    

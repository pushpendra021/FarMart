from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        tractor_parts = Product.objects.filter(category='TPA')
        irrigation_systems = Product.objects.filter(category='IS')
        harvesting_tools = Product.objects.filter(category='HT')
    
        seeds_saplings = Product.objects.filter(category='SS')
        fertilizers_boosters = Product.objects.filter(category='FGB')
        organic_products = Product.objects.filter(category='OFP')
        # You can now return these in context if rendering a template
        context = {
            'tractor_parts': tractor_parts,
            'irrigation_systems': irrigation_systems,
            'harvesting_tools': harvesting_tools,
          
         
            'seeds_saplings': seeds_saplings,
            'fertilizers_boosters': fertilizers_boosters,
            'organic_products': organic_products,
        }
        return render(request, 'app/home.html', context)

# def home(request):
#  return render(request, 'app/home.html')

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False  # Default value

        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)
            ).exists()

        return render(request, 'app/productdetail.html', {
            'product': product,
            'item_already_in_cart': item_already_in_cart
        })


@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('showcart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        if cart:
           for item in cart:
            amount += item.quantity * item.product.selling_price  # fixed here

           total_amount = amount + shipping_amount

           return render(request, 'app/addtocart.html', {
              'carts': cart,
              'amount': amount,
              'totalamount': total_amount
           })
        else:
           return render(request,'app/emptycart.html')
      

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            tempamount = p.quantity * p.product.selling_price
            amount += tempamount
        
        totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            tempamount = p.quantity * p.product.selling_price
            amount += tempamount
        
        totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            tempamount = p.quantity * p.product.selling_price
            amount += tempamount
        
        totalamount = amount + shipping_amount

        data = {
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)
    
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 add=Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active': 'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})




def harvesting_tools(request,data=None):
 if data==None:
   harvesting=Product.objects.filter(category='HT')
 elif data=="LocalForge" or data=="GreenPluck":
   harvesting=Product.objects.filter(category='HT').filter(brand=data)
 elif data == 'below':
    harvesting = Product.objects.filter(category='HT').filter(discounted_price__lt=10000)
 elif data == 'above':
    harvesting= Product.objects.filter(category='HT').filter(discounted_price__gt=10000)
 
 return render(request, 'app/harvesting_tools.html',{'harvesting':harvesting})

#navigation first section done
def tractor_parts(request,data=None):
 if data==None:
   tractor=Product.objects.filter(category='TPA')
 elif data=="AgroLink" or data=="CropSharp" or data=="AgriParts":
   tractor=Product.objects.filter(category='TPA').filter(brand=data) 
 elif data == 'below':
    tractor = Product.objects.filter(category='TPA').filter(discounted_price__lt=10000)
 elif data == 'above':
   tractor = Product.objects.filter(category='TPA').filter(discounted_price__gt=10000)
 
 return render(request, 'app/tractor_parts.html',{'tractor':tractor})

def irrigation_systems(request,data=None):
 if data==None:
   irrigation=Product.objects.filter(category='IS')
 elif data=="model1" or data=="model2" or data=="model3":
   irrigation=Product.objects.filter(category='IS').filter(brand=data) 
 elif data == 'below':
    irrigation= Product.objects.filter(category='IS').filter(discounted_price__lt=10000)
 elif data == 'above':
   irrigation = Product.objects.filter(category='IS').filter(discounted_price__gt=10000)
 
 return render(request, 'app/irrigation_systems.html',{'irrigation':irrigation})


#navigation 2nd section done

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration successful!')
            
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.selling_price
            amount += tempamount

    totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully!')
            

        # if form is not valid, show the same form with errors
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
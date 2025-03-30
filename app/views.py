from django.shortcuts import render
from django.views import View
from .models import Customer,Product,Cart, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

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
        return render(request, 'app/productdetail.html', {'product': product})




def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')



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


def checkout(request):
 return render(request, 'app/checkout.html')




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
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models  import Product,OrderDetaile
from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.edit import CreateView,UpdateView ,DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse
from django.core.paginator import Paginator
import stripe

#request to GATEWAY 
from django.http.response import HttpResponseNotFound,JsonResponse
from django.shortcuts import get_object_or_404
# settings.py
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return HttpResponse("->>Hamidreza<<-")


def products(request):
    products =  Product.objects.all()
    

  
    name_search = request.GET.get("product_name")
    # when don't search and url doesnot contain ?product_name= >> None
    if name_search is not None and name_search.strip() != '' :
        products =  products.filter(name__icontains = name_search.strip())



    # set data
    paginate = Paginator(products,3)
    # get page by request
    page_number = request.GET.get("page")
    # set obj with page_obj
    page_obj = paginate.get_page(page_number)
    context={
        # "products":products
        "page_obj":page_obj
    }
    products = Product.objects.all()
    return render(request,"temp/index.html",context)
    
# products Class
class ProductListView(ListView):
    # ** base on ListView -> ir selects all datas(products) from db
    model =Product
    context_object_name='products'
    template_name="temp/index.html"
    paginate_by=3

def product_detail(request,id):
    item= Product.objects.get(id =id)
    context={
        "item":item,
    }
    return  render(request,"temp/detail.html",context)
# detail Class  

class ProductDetailView(DetailView):
    model=Product
    context_object_name="item"
    template_name="temp/detail.html"

    # gateway
    # PUBLISH_KEY
    pk_url_kwarg = 'pk'
    # use context like function view
    def get_context(self,**kwargs):
        context = super(ProductDeleteView,self).get_context(**kwargs)
        context["stripe_publish_key"]=settings.STRIPE_PUBLISH_KEY
        return context


# SECRET_KEY
# request to stripe >> Cross-Site Req 
@csrf_exempt
def create_checkout_session(req,id):
    #get The product by id!
    product = get_object_or_404(Product,pk=id)
    # pip install stripe
    # import stripe
    # , at end of each line
    # req.user > logged-in user
    stripe.api_key =settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=req.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount':product.price,
                },
                'quantity':1,
            }
        ],
        mode="payment",
        success_url=req.build_absolute_uri(reverse("my_papp:success"))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=req.build_absolute_uri(reverse("my_papp:failed")),
    )
    order=OrderDetaile()
    order.customer_username=req.user.username
    order.product = product
    order.stripe_payment_intent=checkout_session['payment_intent']
    order.amount = product.price
    order.save()
    return JsonResponse({'sessionId':checkout_session.id})



class PaymentSuccessView(TemplateView):
    template_name="myapp/payment_success.html"
    def get(self,request,*args, **kwargs):
        session_id =request.GET.get("session_id")
        if session_id is None:
            return HttpResponseNotFound()
        session= stripe.checkout.Session.retrieve(session_id)
        stripe.api_key= settings.STRIPE_SECRET_KEY 
        order = get_object_or_404(OrderDetaile,stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request,self.template_name)
    
   
class PaymentFailedView(TemplateView):
    template_name="myapp/payment_failed.html"    
@login_required
def add_product(request):
    # POST method to /myapp/products/add/
    if request.method=="POST":
        # currently logged-in user
        seller_name =request.user
        name =request.POST.get("name")
        price =request.POST.get("price")
        desc =request.POST.get("desc")
        image = request.FILES['upload']
        product=Product(name=name,price=price,desc=desc,image=image,seller_name=seller_name)
        product.save()
    # GET Method /myapp/products/add/
    return render(request,"temp/add_product.html")

# class Create 

class ProductCreateView(CreateView):
    model =Product
    fields = ['seller_name',"name",'price','desc','image']
    # not custom template name! **myapp/product_form.html template


def update_product(request,id):



    product=Product.objects.get(id=id)


    if(request.method=='POST'):
        product.name=request.POST.get("name")
        product.price=request.POST.get("price")
        product.desc=request.POST.get("desc")
        product.image=request.FILES["upload"]
        product.save()
        return redirect("/myapp/products")

    context={
        'product':product
    }
    return render(request,"temp/update_product.html",context)    
    
    
# Update class

class ProductUpdateView(UpdateView):
    model=Product
    # it should be in myapp dir
    # custom templatename : product_update_form.html
    fields=['name','price','desc','image']
    template_name_suffix="_update_form"



def delete_product(request,id):
     product=Product.objects.get(id=id)
     context={
         "product":product
     }   
     if(request.method=="POST"):
         product.delete()
         return redirect("/myapp/products")

     return render(request,"temp/delete.html",context)

# Delete Class

class ProductDeleteView(DeleteView):
    model =Product
    success_url = reverse_lazy('my_papp:products')


# Logged-in user products
# Filter -> use conditions!
def my_products(request):
    # only current user products

    products= Product.objects.filter(seller_name=request.user)
    context={
      'products':products
    }
    return render(request,"temp/my_products.html",context)
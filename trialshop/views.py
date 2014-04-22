from django.shortcuts import render ,get_object_or_404
from trialshop.models import Product,catagory,Cart
from django.contrib.auth.models import User
from trialshop.forms import LoginForm,SignupForm,quanti
from django.http import HttpResponse,request
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login,logout
import stripe
from model_mommy import mommy
from django.contrib.auth.decorators import login_required

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'trialshop/new_arrival.html'
    def get(self,request,*args,**kwargs):
        productobj=Product.objects.order_by('-pub_date')
        Pmode=catagory.objects.all()
        if request.user.is_authenticated():
            lencart=len(Cart.objects.filter(user=request.user))
            return self.render_to_response({ 'lencart':lencart, 'pmode' :  Pmode ,   'productobj':productobj ,
            })
        else:
            return self.render_to_response({'pmode' :  Pmode ,   'productobj':productobj ,
            })
class CategoryView(generic.TemplateView):
    template_name = 'trialshop/new_arrival.html'
    def get(self,request,*args,**kwargs):
        # print Product.objects.get(product_type.id==1),"kjhkjkjbk"
        # print catagory.objects.get(id=kwargs['category_id'])
        Pmode=catagory.objects.all()
        
        productobj=Product.objects.all()
        Pmode_search=catagory.objects.get(id=kwargs['category_id'])
        if request.user.is_authenticated():
            lencart=len(Cart.objects.filter(user=request.user))
        else:
            lencart=0
        return self.render_to_response({ 'lencart':lencart, 'pmode' :  Pmode ,   'productobj':productobj ,'Pmode_search' :  Pmode_search ,
            })
        # print kwargs['category_id']
class DescView(generic.TemplateView):
    template_name = 'trialshop/product_detail.html'
    def get(self,request,*args,**kwargs):
        productobj=Product.objects.all()
        Pmode_search=Product.objects.get(id=kwargs['category_id'])
        catagory_ob=catagory.objects.all()
        
        if request.user.is_authenticated():
            lencart=len(Cart.objects.filter(user=request.user))
            return self.render_to_response({ 'lencart': lencart,'Pmode_search' :  Pmode_search ,'catagory_ob':catagory_ob,'quanti':quanti,
            })
        else:
            return self.render_to_response({ 'Pmode_search' :  Pmode_search ,'catagory_ob':catagory_ob,'quanti':quanti,
            })
            
class CartView(generic.TemplateView):
    template_name = 'trialshop/viewbasket.html'
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            cur_usr_cart=Cart.objects.filter(user=request.user)
            cart_prod=[]
            cart= Cart.objects.all()
            prod_obj=Product.objects.all()
            for c in cur_usr_cart:        
                for product in prod_obj:
                    if product.product_name == str(c.product_id):
                        c.pid=product.id
                        c.price=product.product_price
                        p=product.product_price
                        x=c.quantity
                        c.total_val=x*p
                        c.save()
            user=request.user           
            total=0
            leng=len(cur_usr_cart)
            for c in cur_usr_cart:
                total=total+c.total_val
            catagory_ob=catagory.objects.all()
            lencart=len(Cart.objects.filter(user=request.user))
            return self.render_to_response({'lencart':lencart,'user':user,'cur_usr_cart':cur_usr_cart,'total':total,'catagory_ob':catagory_ob,'leng':leng,
            })
        else:
            return  HttpResponseRedirect('/login')

@login_required()
def AddToCart(request,*args,**kwargs):
    # if request.user.is_authenticated():
    x=kwargs['cart_id']
    chk_product=Product.objects.get(id=x)
    if chk_product:
        # x=request.POST['Qunty']
        p=Cart(user=request.user,product_id=chk_product,quantity=1)
        p.save()
    return  HttpResponseRedirect('/cartbasket')
    # else:
    # return  HttpResponseRedirect('/login')
            
def CartRemove(request,*args,**kwargs):
    # print kwargs
    if request.user.is_authenticated():
        x=kwargs['cart_id']
        # print x
        cart_obj= Cart.objects.all()
        for dlt in cart_obj:
            Cart.objects.filter(id=x).delete()
            obj=Cart.objects.filter(user=request.user)
            if len(obj)<1:
                return HttpResponseRedirect('/index')
            else:
                return HttpResponseRedirect('/cartbasket')
    else:
        return  HttpResponseRedirect('/login')

class loginform(generic.TemplateView):
    template_name = 'trialshop/login.html'

    def get(self,request,*args,**kwargs):
        next=request.GET.get('next')
        if request.user.is_authenticated():
            return  HttpResponseRedirect('/index')
        else:
            return self.render_to_response({'LoginForm':LoginForm,'next':next,
            })


def login_request(request):
        form = LoginForm(request.POST) 
        username = request.POST['username']
        password = request.POST['password']
        next=request.POST.get('next',None)
        user = authenticate(username=username, password=password)
        # print request.GET,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",request.GET.get('next')

        if user is not None:
            if user.is_active:
                login(request, user)
                if next:
                    return HttpResponseRedirect(next)

                return HttpResponseRedirect('/index')
            else:
                form = LoginForm()
        else:
            return HttpResponseRedirect('login')



class signup(generic.TemplateView):
    template_name = 'trialshop/signup.html'
    def get(self,request,*args,**kwargs):
            return self.render_to_response({'SignupForm':SignupForm,
        })
class about(generic.TemplateView):
    template_name = 'trialshop/about.html'
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_request(request):
    form = SignupForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    password_confirm=request.POST['password_confirm']
    email=request.POST['email']
    u=User(username=username,password=password,email=email)
    u.save()
    return HttpResponseRedirect('/login')

# def charge_payment(request):
#     cur_usr_cart=Cart.objects.filter(user=request.user)
#     total1 =0
#     for c in cur_usr_cart:
#         total1=total1+c.total_val
#     # Set your secret key: remember to change this to your live secret key in production
#     # See your keys here https://manage.stripe.com/account
#     print "helo owais 1"
#     stripe.api_key = "sk_test_NhO6U7lMQIvidV5EDdgKObPT"

#     # Get the credit card details submitted by the form
#     token = request.POST['stripeToken']
#     # Create the charge on Stripe's servers - this will charge the user's card
#     try:
#      charge = stripe.Charge.create(
#         amount=total1, # amount in cents, again
#         currency="usd",
#         card=token,
#         description="payinguser@example.com"
#     )
#     except stripe.CardError, e:
#     # The card has been declined
#         pass

#     print "helo owais 4"
#     return HttpResponseRedirect('/')     
    
class charge_payment(generic.TemplateView):
    template_name = 'trialshop/about.html'
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            cur_usr_cart=Cart.objects.filter(user=request.user)
            total1 =0
            for c in cur_usr_cart:
                total1=total1+c.total_val
            # Set your secret key: remember to change this to your live secret key in production
            # See your keys here https://manage.stripe.com/account
            print "helo owais 1"
            stripe.api_key = "sk_test_NhO6U7lMQIvidV5EDdgKObPT"

            # Get the credit card details submitted by the form
            token = request.POST['stripeToken']
            # Create the charge on Stripe's servers - this will charge the user's card
            try:
             charge = stripe.Charge.create(
                amount=total1, # amount in cents, again
                currency="usd",
                card=token,
                description="payinguser@example.com"
            )
            except stripe.CardError, e:
            # The card has been declined
                pass

            print "helo owais 4"
            return self.render_to_response({'user':user,'cur_usr_cart':cur_usr_cart,'total':total,'catagory_ob':catagory_ob,'leng':leng,
            })
        else:
            return  HttpResponseRedirect('/login')


# Create your tests here.
# pro=mommy.make('Product',_quantity=3)
# cat=mommy.make('catagory',_quantity=3)
# car=mommy.make('Cart',_quantity=3)
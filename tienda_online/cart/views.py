from django.shortcuts import render, get_object_or_404
from .cart import Cart  

from tienda.models import Product 
from django.http import JsonResponse 
# Create your views here.
def cart_summary(request):  
    cart=Cart(request) 
    cart_products=cart.get_products
    return render(request, "cart_summary.html",{"cart_products":cart_products}) 


def cart_add(request):  
    #traemos el carro 
    cart=Cart(request) 
    #hacemos test para el post 
    if request.POST.get('action')=='post': 
        product_id=int(request.POST.get('product_id')) 
        #buscamos el producto en la base de datos 
        product=get_object_or_404(Product,id=product_id)
        #guardamos en la sesion 
        cart.add(product=product)  
        cart_quantity=cart.__len__()
        
        response=JsonResponse({'qty: ':cart_quantity}) 
        return response
    


def add_to_cart(request): 
    cart_product={}  
    
    cart_product[str(request.GET['id'])]={ 
        'title':request.GET['title'],
        'qty': request.GET['qty'],  
        'price':request.GET['price']
        
        } 
    
    if 'cart_data_obj' in request.session: 
        if str(request.GET['id']) in request.session['cart_data_obj']: 
            cart_data=request.session['cart_data_obj'] 
            cart_data[str(request.GET['id'])]['qty']=int(cart_product[str(request.GET['id'])]['qty']) 
            cart_data.update(cart_data) 
            request.session['cart_data_obj']=cart_data 
        else: 
            cart_data=request.session['cart_data_obj'] 
            cart_data.update(cart_product) 
            request.session['cart_data_obj']=cart_data 
    else: 
        request.session['cart_data_obj']=cart_product 
    return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj'])}) 

    
def cart_delete(request): 
    pass 

def cart_update(request): 
    pass 

 




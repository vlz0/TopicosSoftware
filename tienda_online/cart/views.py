from django.shortcuts import render, get_object_or_404,redirect
from .cart import Cart  
from django.contrib import messages 
from tienda.models import Product 
from django.http import JsonResponse  
from django.template.loader import render_to_string
# Create your views here. 


def add_to_cart(request): 
    cart_product={}   
    qty = int(request.GET['qty'])
    price = float(request.GET['price'])
    
    total_price = qty * price
    
    cart_product[str(request.GET['id'])]={ 
        'title':request.GET['title'],
        'qty': request.GET['qty'],  
        'price':request.GET['price'], 
        'image':request.GET['image'], 
        'total_price': total_price,
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

     
     


def cart_view(request):  
    cart_total_amount = 0 
    if 'cart_data_obj' in request.session: 
        for product_id, item in request.session['cart_data_obj'].items(): 
            try:
                # Intenta convertir el precio a float
                price = float(item['price'])
                qty = int(item['qty'])
                # Suma el costo total del producto al total del carrito
                cart_total_amount += qty * price
            except ValueError:
                # Maneja el caso en que el precio no sea un número válido
                pass
        return render(request, 'cart.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount,}) 
    else: 
        messages.success(request, "El carrito está vacío") 
        return redirect('home')

def cart_delete(request): 
    product_id=str(request.GET['id']) 
    if 'cart_data_obj'in request.session: 
        if product_id  in request.session['cart_data_obj']: 
            cart_data=request.session['cart_data_obj'] 
            del request.session['cart_data_obj'][product_id] 
            request.session['cart_data_obj']=cart_data  
    
    cart_total_amount=0 
    if 'cart_data_obj' in request.session: 
        for product_id, item in request.session['cart_data_obj'].items(): 
            try:
                # Intenta convertir el precio a float
                price = float(item['price'])
                qty = int(item['qty'])
                # Suma el costo total del producto al total del carrito
                cart_total_amount += qty * price
            except ValueError:
                # Maneja el caso en que el precio no sea un número válido
                pass 
    
    context=render_to_string("cart-list.html",{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount,}) 
    return JsonResponse({"data":context,'totalcartitems': len(request.session['cart_data_obj'])})





def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        if product_id and action:
            if 'cart_data_obj' in request.session:
                cart_data = request.session['cart_data_obj']
                if product_id in cart_data:
                    if action == 'add':
                        cart_data[product_id]['qty'] = str(int(cart_data[product_id]['qty']) + 1) 
                        cart_data[product_id]['total_price'] = str(float(cart_data[product_id]['qty']) * float(cart_data[product_id]['price']))
                    elif action == 'subtract':
                        # Restar la cantidad y verificar si es cero
                        cart_data[product_id]['qty'] = str(int(cart_data[product_id]['qty']) - 1)
                        if int(cart_data[product_id]['qty']) == 0:
                            del cart_data[product_id]  # Eliminar el producto del carrito si la cantidad es cero
                        else:
                            # Actualizar el precio total del producto si la cantidad no es cero
                            cart_data[product_id]['total_price'] = str(float(cart_data[product_id]['qty']) * float(cart_data[product_id]['price']))
                    request.session['cart_data_obj'] = cart_data
    return redirect('cart_view')




 
 




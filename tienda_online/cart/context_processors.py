from .cart import Cart 

#creamos el context processor 
def cart(request): 
    return {'cart':Cart(request)}
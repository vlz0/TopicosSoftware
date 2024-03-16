#vamos a hacer la creacion de la variable global para que se almacene siempre 
def importe_total_carro(request):  
    total=0
    #if request.user.is_authenticated: #primero vamos a mirar que el usuario este ya ingrasado  
    if 'carro'in request.session: 
        for key, value in request.session["carro"].items(): 
            
            total=total+(float(value["precio"])) #que aumente el total cada vez que se va recorriendo uno por uno 
    return {"importe_total_carro":total}
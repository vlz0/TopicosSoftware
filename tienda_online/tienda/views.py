from django.shortcuts import render,redirect
from .models import Product, Categoria
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages  
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.views.generic import View  
from .forms import *
# Create your views here.
def home(request): 
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})   





def login_user(request):  
    if request.method =='POST': 
        usuario=request.POST['usuario'] 
        contraseña=request.POST['contraseña'] 
        user=authenticate(request,username=usuario, password=contraseña) 
        if user is not None: 
            login(request,user) 
            messages.success(request,("Ha ingresado exitosamente!")) 
            return redirect ('home')
        else: 
            messages.success(request,("Hubo un error, por favor intente de nuevo")) 
            return redirect ('home') 
    else: 
        return render(request,'login.html',{})
    




"""def register_user(request): 
    return render(request,'register.html',{})
"""


def logout_user(request):  
    logout(request)  
    messages.success(request,("Ha cerrado la sesión!"))
    return redirect('home') 

class VRegistro(View): 
    def get(self,request):  
        form=CustomUserCreationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request): 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario=form.save() 
            login(request,usuario)  
            messages.success(request,("Su usuario se ha creado exitosamente"))  
            return redirect('home') 
            
        else: 
            for msg in form.error_messages: #se deben recorrer todos los errores que se prersenten y por cada uno que haya lo debe de mostrar 
                messages.error(request,form.error_messages[msg]) #se llama al messages.error para que mire los que hay en la peticion y en el formulario 
            return render(request,"register.html",{"form":form}) #que devuelva al formulario 
        


def product(request,pk): 
    product=Product.objects.get(id=pk) 
    return render(request,"product.html",{"product":product})  


def category(request,foo): 
    foo=foo.replace('-',' ') 
    #traemos la categoria de la url 
    try:  
        category=Categoria.objects.get(nombre=foo) 
        products= Product.objects.filter(category=category) 
        return render(request,'category.html',{'products':products, 'category':category}) 
    
    
    except:  
        messages.success(request,("Esa categoria no existe")) 
        return redirect ('home')
    
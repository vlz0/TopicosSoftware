from django.db import models 
import datetime

# Create your models here.

#categoria de cada producto
class Categoria(models.Model): 
    nombre=models.CharField(max_length=50)   
    def __str__(self): 
        return self.nombre
    

#usuario
class Client(models.Model): 
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    cell= models.CharField(max_length=10) 
    email= models.EmailField(max_length=100) 
    password= models.CharField(max_length=100)
    
    def __str__(self): 
        return f'{self.first_name}{self.last_name}' 
     
    

#producto
class Product(models.Model): 
    name= models.CharField(max_length=100)
    price=models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category= models.ForeignKey(Categoria,on_delete=models.CASCADE, default=1) 
    
    description=models.CharField(max_length=250,default='', blank=True,null=True) 
    
    image= models.ImageField(upload_to='uploads/product') 
    
    #se agregan los descuentos 
    is_sale=models.BooleanField(default=False) 
    sale_price=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    
    def __str__(self): 
        return self.name 

#orden
class Orden(models.Model): 
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    client= models.ForeignKey(Client,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
    address= models.CharField(max_length=100, default='',blank=True) 
    phone =models.CharField(max_length=20,default='',blank=True)
    date =models.DateField(default=datetime.datetime.today)
    satus= models.BooleanField(default=False)
    
    def __str__(self): 
        return self.product
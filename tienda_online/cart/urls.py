

from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path,include 
from . import views 

urlpatterns = [
    
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),  
    path('delete-product/',views.cart_delete,name="delete-product"),   
    path('update-cart/',views.update_cart,name="update-cart"),
    path('cart_view/',views.cart_view,name="cart_view"),

]


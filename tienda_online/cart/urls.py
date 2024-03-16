

from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path,include 
from . import views 

urlpatterns = [
    path('cart/', views.cart_summary,name='cart_summary'),  
    path('add/', views.cart_add,name='cart_add'), 
    path('delete/', views.cart_delete,name='cart_delete'),
    path('update/', views.cart_update,name='cart_update'), 
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),

]


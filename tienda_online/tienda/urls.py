from django.contrib import admin
from django.urls import path,include 
from . import views 
from .views import VRegistro

urlpatterns = [
    path('', views.home,name='home'),  
    path('login/', views.login_user,name='login'), 
    path('logout/', views.logout_user,name='logout'), 
    path('register/', VRegistro.as_view(),name='register'), 
    path('product/<int:pk>', views.product,name='product'), 
    path('category/<str:foo>', views.category,name='category'),
]
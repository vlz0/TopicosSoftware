from django.urls import path
from . import views 
from .views import VRegistro, ProductSearchListView, ProductListAPI,AlliedBrandsView

urlpatterns = [
    path('', views.home,name='home'),  
    path('login/', views.login_user,name='login'), 
    path('logout/', views.logout_user,name='logout'), 
    path('register/', VRegistro.as_view(),name='register'), 
    path('product/<int:pk>', views.product,name='product'),
    path('addProduct', views.addProduct,name='addProduct'), 
    path('category/<str:foo>', views.category,name='category'),

    path('search/', ProductSearchListView.as_view(), name='search'),
    path('api/products/', ProductListAPI.as_view(), name='product-list-api'), 
    path('allied-brands/', AlliedBrandsView.as_view(), name='allied_brands'),
]

from django.contrib import admin
from .models import *


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']  # Mostrar el nombre en la lista
    search_fields = ['nombre']  # Permitir la búsqueda por nombre
    fields = ['nombre']  # Campos a mostrar en el formulario de edición

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_sale', 'sale_price']  # Campos a mostrar en la lista
    list_filter = ['category', 'is_sale']  # Permitir filtrar por categoría y estado de venta
    search_fields = ['name', 'description', 'category__nombre']  # Permitir la búsqueda por nombre de producto, descripción o nombre de categoría
    fields = ['name', 'price', 'category', 'description', 'image', 'is_sale', 'sale_price']  # Campos a mostrar en el formulario de edición


class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'cell', 'email']  # Campos a mostrar en la lista
    search_fields = ['first_name', 'last_name', 'email', 'cell']  # Permitir la búsqueda por nombre, apellido, email o celular
    list_filter = ['email']  # Permitir filtrar por email
    fields = ['first_name', 'last_name', 'cell', 'email', 'password']  # Campos a mostrar en el formulario de edición

class OrdenAdmin(admin.ModelAdmin):
    list_display = ['get_product_name', 'client', 'quantity', 'address', 'phone', 'date', 'satus']  # Campos a mostrar en la lista
    list_filter = ['date', 'satus', 'client']  # Permitir filtrar por fecha, estado y cliente
    search_fields = ['product__name', 'client__first_name', 'client__last_name', 'address']  # Permitir la búsqueda por nombre de producto, nombre de cliente, apellido de cliente o dirección

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.admin_order_field = 'product'  # Permitir ordenar por nombre de producto
    get_product_name.short_description = 'Nombre del Producto'  # Texto a mostrar en la cabecera de la columna

    # Campos a mostrar en el formulario de edición
    fields = ['product', 'client', 'quantity', 'address', 'phone', 'date', 'satus']


# Registrar los modelos y sus clases de administración correspondientes
admin.site.register(Orden, OrdenAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Categoria, CategoriaAdmin)  
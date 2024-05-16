from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'created_at', 'pdf_file')
    search_fields = ('customer_name', 'customer_email')


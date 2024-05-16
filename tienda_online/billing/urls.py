from django.urls import path
from .views import view_bill, download_bill, send_bill_email

app_name = "billing"

urlpatterns = [
    path('generate_bill/', view_bill, name='generate_bill'),
    path('download-bill/<int:bill_id>/', download_bill, name='download-bill'),
    path('send-bill/<int:bill_id>/', send_bill_email, name='send-bill'),

]

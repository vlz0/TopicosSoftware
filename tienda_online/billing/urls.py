from django.urls import path
from .views import bill_view

app_name = "billing"

urlpatterns = [
    path('generate_bill/', bill_view, name='generate_bill'),
]

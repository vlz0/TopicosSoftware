from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_view_url(self, obj):
        return f"http://127.0.0.1:8000/product/{obj.id}"
from .models import Product, cart
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = ['total_price', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True}  # Owner can be set later, not required at creation
        }
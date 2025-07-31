from .models import Product, cart
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'
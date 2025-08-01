from django.shortcuts import render
from .serializers import ProductSerializer, CartSerializer
from django.contrib.auth.models import User
from .models import Product, cart
from rest_framework import generics, permissions

# Create your views here.
# This view allows users to view all products
class ViewProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

# This view allows users to view specific products
class ProductDetails(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

# This view allows users to add products to their cart
class CartSys(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]    
    lookup_field = 'owner'

    def get_queryset(self):
        user = self.request.user
        queryset = cart.objects.filter(owner=user)
        return queryset
    
    
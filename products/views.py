from django.shortcuts import render
from .serializers import ProductSerializer, CartSerializer
from django.contrib.auth.models import User
from .models import Product, cart
from rest_framework import generics, permissions

# Create your views here.

class ViewProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]#come change this before production

class ProductDetails(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class CartSys(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]    #come change this efore production
    lookup_field = 'owner'

    def get_queryset(self):
        user = self.request.user
        queryset = cart.objects.filter(owner=user)
        return queryset
    
    
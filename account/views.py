from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.
#This is the view for user registration
class register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
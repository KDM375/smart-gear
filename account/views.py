from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.
#This is the view for user registration
class register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def index(request):
        if request.user.is_authenticated:
            return JsonResponse({"email": "{request.user.email}"}, status=200)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
   
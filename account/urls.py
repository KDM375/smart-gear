from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.register.as_view()), #this is for signup
    path('token/', TokenObtainPairView.as_view()), # this is for login
    path('token_refresh/', TokenRefreshView.as_view()) # this is the endpoint for refreshing expired tokens
]
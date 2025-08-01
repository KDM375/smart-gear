from django.urls import path
from . import views

urlpatterns = [
    path('initiate/', views.Checkout.as_view(), name='payment'), # Endpoint to initiate payment to paystack and get authorization URL
    path('success/', views.payment_success), # incase of successful payment
    path('failure/', views.payment_failed), # incase of failed payment
    path('webhooks/', views.Webhook_handler.as_view()) # Endpoint to handle Paystack webhooks
]

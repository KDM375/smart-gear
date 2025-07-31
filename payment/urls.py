from django.urls import path
from . import views

urlpatterns = [
    path('initiate/', views.Checkout.as_view(), name='payment'),
    path('success/', views.payment_success),
    path('failure/', views.payment_failed),
    #path('webhooks/', views.webhook_handler)
]

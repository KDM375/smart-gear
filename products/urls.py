from django.urls import path
from . import views

urlpatterns = [
    path('all_products/', views.ViewProducts.as_view()),
    path('cart/', views.CartSys.as_view()),
    path('item/<int:id>/', views.ProductDetails.as_view())
]
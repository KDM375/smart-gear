from django.urls import path
from . import views

urlpatterns = [
    path('all_products/', views.ViewProducts.as_view()), # this shows all the products in stock
    path('cart/', views.CartSys.as_view()), # shows all the items placed in the cart
    path('item/<int:id>/', views.ProductDetails.as_view()) # it shows more details on a product
]
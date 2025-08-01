from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#This is the product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length= 100)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=20)
    stock = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='img')

    def __str__(self):
        return self.name
    
#this is the cart model
class cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.TextField()
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.items

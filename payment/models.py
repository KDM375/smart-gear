from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    owner = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)  # e.g., 'card' or 'momo'
    status = models.CharField(max_length=50)  # e.g., 'completed', 'pending', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amount
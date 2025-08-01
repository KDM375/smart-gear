from rest_framework import serializers
from .models import Transaction

# this serializer transforms the Transaction model into JSON format and vice versa
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


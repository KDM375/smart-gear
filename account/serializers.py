from rest_framework import serializers
from django.contrib.auth.models import User

# we use this serializer to transform the pre-built User model into json data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, data):
        return User.objects.create_user(**data)
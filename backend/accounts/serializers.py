from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','role','is_active']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','role']
    
    def validate(self, value):
        
        if value == 'ADMIN':
            raise serializers.ValidationError(
                "Admin accounts can not be created"
            )
        
        return value
    
    def create(self, validate_data):

        user = User.objects.create(
            username= validate_data['username'],
            email=validate_data['email'],
            role=validate_data['role']
        )
        return user

 
class CreatePasswordSerializer(serializers.Serializer):

    password = serializers.CharField( required = True, write_only=True)


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        user = authenticate(
            username = data['username'],
            password = data['password']
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid Credentials"
            )
        
        data['user'] = user

        return data
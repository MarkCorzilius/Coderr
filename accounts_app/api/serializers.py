from rest_framework import serializers
from accounts_app.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):

        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        
        try:
            validate_password(data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})
        
        return data

    
    def create(self, validated_data):

        validated_data.pop('repeated_password')

        return User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
        )



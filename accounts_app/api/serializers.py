from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from accounts_app.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serialize and validate new user registration data."""

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "repeated_password", "type"]

    def validate(self, data):
        """Validate password match, strength, and field uniqueness."""

        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        try:
            validate_password(data["password"])
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        return data

    def create(self, validated_data):
        """Create a new user from validated data."""

        validated_data.pop("repeated_password")
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class LoginSerializer(serializers.ModelSerializer):
    """Serialize user data returned after successful login."""

    user_id = serializers.IntegerField(source="id", read_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["token", "username", "email", "user_id"]

    def get_token(self, obj):
        """Return authentication token key from context."""

        return self.context["token"].key
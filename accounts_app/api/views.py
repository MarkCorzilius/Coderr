from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import Throttled
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts_app.api.serializers import LoginSerializer, RegisterSerializer
from accounts_app.api.throttles import LoginRateThrottle, RegisterRateThrottle


class RegisterView(CreateAPIView):
    """Handle user registration and token creation."""

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    throttle_classes = [RegisterRateThrottle]

    def throttled(self, request, wait):
        """Raise friendly error when rate limit is exceeded."""

        raise Throttled(
            detail="Too many registration attempts. Please try again later.",
            wait=wait,
        )

    def post(self, request, *args, **kwargs):
        """Register a new user and return auth token."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(CreateAPIView):
    """Handle user login and return auth token."""

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    throttle_classes = [LoginRateThrottle]

    def throttled(self, request, wait):
        """Raise friendly error when rate limit is exceeded."""

        raise Throttled(
            detail="Too many login attempts. Please try again later.",
            wait=wait,
        )

    def post(self, request, *args, **kwargs):
        """Authenticate user credentials and return token."""

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        token, _ = Token.objects.get_or_create(user=user)
        serializer = self.serializer_class(user, context={"token": token})
        return Response(serializer.data, status=status.HTTP_200_OK)
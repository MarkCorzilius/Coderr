from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts_app.api.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from accounts_app.api.throttles import RegisterRateThrottle
from rest_framework.exceptions import Throttled

class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    throttle_classes = [RegisterRateThrottle]

    def throttled(self, request, wait):
        raise Throttled(
            detail="Too many registration attempts. Please try again later.",
            wait=wait
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.email,
            "email": user.email,
            "user_id": user.id
        })
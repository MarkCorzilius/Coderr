from rest_framework.generics import RetrieveUpdateAPIView
from profile_app.api.serializers import ProfileSerializer
from profile_app.models import Profile
from rest_framework.permissions import IsAuthenticated
from profile_app.api.permissions import IsProfileOwner
from rest_framework.authentication import TokenAuthentication

class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user_id'

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsProfileOwner()]
        return [IsAuthenticated()]



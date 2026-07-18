from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from profile_app.api.serializers import ProfileDetailSerializer, ProfileListSerializer
from profile_app.models import Profile
from rest_framework.permissions import IsAuthenticated
from profile_app.api.permissions import IsProfileOwner
from rest_framework.authentication import TokenAuthentication

class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'user_id'

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsProfileOwner()]
        return [IsAuthenticated()]


class BusinessProfilesListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user__type='business')


class CustomerProfilesListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user__type='customer')
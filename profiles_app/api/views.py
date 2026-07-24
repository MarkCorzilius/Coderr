from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from profiles_app.api.permissions import IsProfileOwner
from profiles_app.api.serializers import ProfileDetailSerializer, ProfileListSerializer
from profiles_app.models import Profile


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Retrieve or update a single user profile."""

    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = "user_id"

    def get_permissions(self):
        """Require ownership for PATCH; authenticated for GET."""

        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsProfileOwner()]
        return [IsAuthenticated()]


class BusinessProfilesListAPIView(ListAPIView):
    """List all profiles belonging to business users."""

    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only business-type user profiles."""

        return self.queryset.filter(user__type="business")


class CustomerProfilesListAPIView(ListAPIView):
    """List all profiles belonging to customer users."""

    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only customer-type user profiles."""

        return self.queryset.filter(user__type="customer")
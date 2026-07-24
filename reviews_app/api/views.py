from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from reviews_app.api.permissions import IsAuthenticatedCustomer, IsAuthenticatedReviewCreator
from reviews_app.api.serializers import (
    BaseReviewSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
)
from reviews_app.models import Review


class ReviewViewSet(ModelViewSet):
    """ViewSet for listing, creating, updating and deleting reviews."""

    queryset = Review.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["updated_at", "rating"]
    filterset_fields = ["business_user_id", "reviewer_id"]

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""

        if self.action == "list":
            return BaseReviewSerializer
        if self.action == "create":
            return ReviewCreateSerializer
        if self.action in ["update", "partial_update"]:
            return ReviewUpdateSerializer
        return BaseReviewSerializer

    def get_permissions(self):
        """Return permissions based on the current action."""

        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAuthenticatedCustomer()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticatedReviewCreator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Save review with the current user as reviewer."""

        serializer.save(reviewer=self.request.user)
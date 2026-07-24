from rest_framework.viewsets import ModelViewSet
from reviews_app.models import Review
from reviews_app.api.serializers import BaseReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from reviews_app.api.permissions import IsAuthenticatedCustomer, IsAuthenticatedReviewCreator
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ReviewViewSet(ModelViewSet):

    queryset = Review.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['updated_at', 'rating']
    filterset_fields = ['business_user_id', 'reviewer_id']


    def get_serializer_class(self):
        if self.action == 'list':
            return BaseReviewSerializer
        if self.action == 'create':
            return ReviewCreateSerializer
        if self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer
        return BaseReviewSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticatedCustomer()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticatedReviewCreator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
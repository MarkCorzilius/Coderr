from django.db.models import Min
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from offers_app.api.permissions import IsBusinessUser, IsOfferOwner
from offers_app.api.serializers import (
    OfferCreateUpdateSerializer,
    OfferDetailSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
)
from offers_app.models import Offer, OfferDetail
from offers_app.pagination import OfferPagination


class OfferViewSet(ModelViewSet):
    """ViewSet for listing, creating, retrieving, updating and deleting offers."""

    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["min_price", "updated_at"]

    def get_serializer_class(self):
        """Return the appropriate serializer based on the current action."""

        if self.action == "list":
            return OfferListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return OfferCreateUpdateSerializer
        return OfferRetrieveSerializer

    def get_permissions(self):
        """Return permissions based on the current action."""

        if self.action == "list":
            return [AllowAny()]
        if self.action == "create":
            return [IsBusinessUser()]
        if self.action == "retrieve":
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOfferOwner()]
        return [AllowAny()]

    def get_queryset(self):
            qs = Offer.objects.annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days"),
            )
    
            creator_id = self.request.query_params.get("creator_id")
            if creator_id:
                qs = qs.filter(user_id=creator_id)
    
            max_delivery_time = self.request.query_params.get("max_delivery_time")
            if max_delivery_time:
                try:
                    max_delivery_time = int(max_delivery_time)
                except ValueError:
                    raise ValidationError({"max_delivery_time": "Must be a valid integer."})
                qs = qs.filter(min_delivery_time__lte=max_delivery_time)
    
            min_price = self.request.query_params.get("min_price")
            if min_price:
                try:
                    min_price = int(min_price)
                except ValueError:
                    raise ValidationError({"min_price": "Must be a valid integer."})
                qs = qs.filter(min_price__gte=min_price)
    
            return qs

    def perform_create(self, serializer):
        """Save new offer with the current user as owner."""

        serializer.save(user=self.request.user)
        

class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
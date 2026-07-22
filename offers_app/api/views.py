from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferListSerializer, OfferCreateUpdateSerializer, OfferRetrieveSerializer, OfferDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from offers_app.api.permissions import IsOfferOwner, IsBusinessUser
from offers_app.pagination import OfferPagination
from django.db.models import Min
from rest_framework import filters


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['min_price', 'updated_at']
    filterset_fields = ['creator_id', 'min_price', 'max_delivery_time'] 

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return OfferCreateUpdateSerializer
        if self.action == 'retrieve':
            return OfferRetrieveSerializer
        return OfferRetrieveSerializer
        
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        if self.action == 'create':
            return [IsBusinessUser()]
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update']:
            return [IsOfferOwner()]
        if self.action == 'destroy':
            return [IsOfferOwner()]
        return [AllowAny()]
        
    def get_queryset(self):
        qs = Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days'),
        )
        
        creator_id = self.request.query_params.get("creator_id")
        if creator_id:
            qs = qs.filter(user_id=creator_id)

        max_delivery_time = self.request.query_params.get("max_delivery_time")
        if max_delivery_time:
            qs = qs.filter(min_delivery_time__lte=max_delivery_time)

        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
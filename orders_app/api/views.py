from rest_framework import viewsets
from orders_app.models import Order
from orders_app.api.serializers import OrderListCreateSerializer, OrderUpdateSerializer
from orders_app.api.permissions import IsAuthenticatedBusinessUser, IsAuthenticatedCustomerUser, IsAuthenticatedStaffUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return OrderListCreateSerializer
        if self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderUpdateSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticatedCustomerUser()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticatedBusinessUser()]
        if self.action == 'destroy':
            return [IsAuthenticatedStaffUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if self.action == 'list':
            return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))
        else:
            return Order.objects.all()
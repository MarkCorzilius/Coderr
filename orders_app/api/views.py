from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from orders_app.models import Order
from orders_app.api.serializers import OrderListCreateSerializer, OrderUpdateSerializer, OrderCountSerializer, CompletedOrderCountSerializer
from orders_app.api.permissions import IsAuthenticatedBusinessOwnerUser, IsAuthenticatedCustomerUser, IsAuthenticatedStaffUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response


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
            return [IsAuthenticatedBusinessOwnerUser()]
        if self.action == 'destroy':
            return [IsAuthenticatedStaffUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if self.action == 'list':
            return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))
        else:
            return Order.objects.all()


class OrderCountView(GenericAPIView):
    serializer_class = OrderCountSerializer
    permission_classes = [IsAuthenticatedBusinessOwnerUser]
    lookup_field = "business_user_id"

    def get(self, request, business_user_id):
        count = Order.objects.filter(
            business_user=request.user,
            status="in_progress"
        ).count()
        serializer = self.get_serializer({
            "order_count": count
        })
        return Response(serializer.data)


class CompletedOrderCountView(GenericAPIView):
    serializer_class = CompletedOrderCountSerializer
    permission_classes = [IsAuthenticatedBusinessOwnerUser]
    lookup_field = "business_user_id"

    def get(self, request, business_user_id):
        count = Order.objects.filter(
            business_user=request.user,
            status="completed"
        ).count()
        serializer = self.get_serializer({
            "completed_order_count": count
        })
        return Response(serializer.data)

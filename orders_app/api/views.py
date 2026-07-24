from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders_app.api.permissions import (
    IsAuthenticatedBusinessOwnerUser,
    IsAuthenticatedCustomerUser,
    IsAuthenticatedStaffUser,
)
from orders_app.api.serializers import (
    CompletedOrderCountSerializer,
    OrderCountSerializer,
    OrderListCreateSerializer,
    OrderUpdateSerializer,
)
from orders_app.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for listing, creating, updating and deleting orders."""

    queryset = Order.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""

        if self.action in ["list", "create"]:
            return OrderListCreateSerializer
        return OrderUpdateSerializer

    def get_permissions(self):
        """Return permissions based on the current action."""

        if self.action == "create":
            return [IsAuthenticatedCustomerUser()]
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticatedBusinessOwnerUser()]
        if self.action == "destroy":
            return [IsAuthenticatedStaffUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Return orders visible to the current user."""

        user = self.request.user
        if self.action == "list":
            return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))
        return Order.objects.all()


class OrderCountView(GenericAPIView):
    """Return the number of in-progress orders for a business user."""

    serializer_class = OrderCountSerializer
    permission_classes = [IsAuthenticatedBusinessOwnerUser]
    lookup_field = "business_user_id"

    def get(self, request, business_user_id):
        """Return in-progress order count for the authenticated business user."""

        count = Order.objects.filter(
            business_user=request.user, status="in_progress"
        ).count()
        serializer = self.get_serializer({"order_count": count})
        return Response(serializer.data)


class CompletedOrderCountView(GenericAPIView):
    """Return the number of completed orders for a business user."""

    serializer_class = CompletedOrderCountSerializer
    permission_classes = [IsAuthenticatedBusinessOwnerUser]
    lookup_field = "business_user_id"

    def get(self, request, business_user_id):
        """Return completed order count for the authenticated business user."""

        count = Order.objects.filter(
            business_user=request.user, status="completed"
        ).count()
        serializer = self.get_serializer({"completed_order_count": count})
        return Response(serializer.data)

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

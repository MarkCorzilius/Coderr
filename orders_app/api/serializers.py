from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class BaseOrderSerializer(serializers.ModelSerializer):
    """Base serializer with all order fields."""

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]


class OrderListCreateSerializer(BaseOrderSerializer):
    """Serialize order list and creation via offer detail reference."""

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(),
        source="offer_detail",
        write_only=True,
    )

    class Meta(BaseOrderSerializer.Meta):
        fields = BaseOrderSerializer.Meta.fields + ["offer_detail_id"]
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """Create an order from the referenced offer detail."""

        offer_detail = validated_data.pop("offer_detail")
        return Order.objects.create(
            customer_user=self.context["request"].user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serialize order status updates."""

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
        ]


class OrderCountSerializer(serializers.Serializer):
    """Serialize in-progress order count for a business user."""

    order_count = serializers.IntegerField(read_only=True)


class CompletedOrderCountSerializer(serializers.Serializer):
    """Serialize completed order count for a business user."""

    completed_order_count = serializers.IntegerField(read_only=True)


class OrderListCreateSerializer(BaseOrderSerializer):

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(),
        source='offer_detail',
        write_only=True,
    )
    
    class Meta(BaseOrderSerializer.Meta):
        fields = BaseOrderSerializer.Meta.fields + ["offer_detail_id"]
        read_only_fields=[
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
            ]

    def create(self, validated_data):
        offer_detail = validated_data.pop('offer_detail')
        order = Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )
        return order

class OrderUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['status']
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
            ]

class OrderCountSerializer(serializers.Serializer):
    order_count = serializers.IntegerField(read_only=True)

class CompletedOrderCountSerializer(serializers.Serializer):
    completed_order_count = serializers.IntegerField(read_only=True)
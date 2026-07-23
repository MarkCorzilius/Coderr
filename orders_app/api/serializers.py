from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetail


class BaseOrderSerializer(serializers.ModelSerializer):

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
from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from accounts_app.models import User


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'read_only': True}
            }


class OfferDetailSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = OfferDetail
        fields = [ 
            "id",
            "title", 
            "revisions", 
            "delivery_time_in_days", 
            "price", 
            "features", 
            "offer_type",
            ]


class OfferListSerializer(serializers.ModelSerializer):

    details = OfferDetailHyperlinkedSerializer(many=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)
    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Offer
        fields = [
            "id", 
            "user", 
            "title", 
            "image", 
            "description", 
            "created_at", 
            "updated_at", 
            "details",
            "min_price", 
            "min_delivery_time",
            'user_details'
            ]
        
        read_only_fields = ['id', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']
        

class OfferCreateUpdateSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
            ]
        
        read_only_fields = ['id']
        
    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for detail_data in details_data:
            detail_id = detail_data.get("id")
            if not detail_id:
                raise serializers.ValidationError({"details": "Each detail update requires an id."})
            detail = OfferDetail.objects.get(id=detail_id, offer=instance)
            for attr, value in detail_data.items():
                if attr != "id":
                    setattr(detail, attr, value)
            detail.save()   

        return instance
        

class OfferRetrieveSerializer(serializers.ModelSerializer):

    details = OfferDetailHyperlinkedSerializer(many=True, read_only=True)
    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            ]
        
        read_only_fields = ['id', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']
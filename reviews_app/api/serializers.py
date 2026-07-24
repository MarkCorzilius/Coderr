from rest_framework import serializers
from reviews_app.models import Review


class BaseReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
            ]


class ReviewCreateSerializer(BaseReviewSerializer):

    class Meta(BaseReviewSerializer.Meta):
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']


class ReviewUpdateSerializer(BaseReviewSerializer):

    class Meta(BaseReviewSerializer.Meta):
        read_only_fields = ['id', 'business_user', 'reviewer', 'created_at', 'updated_at']
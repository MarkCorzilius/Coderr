from rest_framework import serializers

from reviews_app.models import Review


class BaseReviewSerializer(serializers.ModelSerializer):
    """Base serializer exposing all review fields."""

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
    """Serialize review creation and prevent duplicate reviews."""

    class Meta(BaseReviewSerializer.Meta):
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, attrs):
        """Ensure the reviewer has not already reviewed this business."""

        reviewer = self.context["request"].user
        business_user = attrs["business_user"]
        if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError("You have already reviewed this profile.")
        return attrs


class ReviewUpdateSerializer(BaseReviewSerializer):
    """Serialize partial review updates (rating and description only)."""

    class Meta(BaseReviewSerializer.Meta):
        read_only_fields = ["id", "business_user", "reviewer", "created_at", "updated_at"]


class ReviewCreateSerializer(BaseReviewSerializer):

    class Meta(BaseReviewSerializer.Meta):
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, attrs):
        reviewer = self.context["request"].user
        business_user = attrs["business_user"]
        if Review.objects.filter(
            reviewer=reviewer,
            business_user=business_user
        ).exists():
            raise serializers.ValidationError(
            "You have already reviewed this profile."
        )
        return attrs


class ReviewUpdateSerializer(BaseReviewSerializer):

    class Meta(BaseReviewSerializer.Meta):
        read_only_fields = ['id', 'business_user', 'reviewer', 'created_at', 'updated_at']
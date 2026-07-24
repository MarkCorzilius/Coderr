from django.db import models
from accounts_app.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer_reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1), MaxValueValidator(5)
            ]
            )
    description = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business_user", "reviewer"],
                name="unique_review_per_business"
            )
        ]
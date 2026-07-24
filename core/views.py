from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts_app.models import User
from offers_app.models import Offer
from reviews_app.models import Review


class BaseInfoAPIView(APIView):
    """Return aggregated platform statistics."""

    permission_classes = [AllowAny]

    def get(self, request):
        """Handle GET request and return platform stats."""

        data = {
            "review_count": Review.objects.count(),
            "average_rating": Review.objects.aggregate(avg=Avg("rating"))["avg"] or 0,
            "business_profile_count": User.objects.filter(type="business").count(),
            "offer_count": Offer.objects.count(),
        }
        return Response(data)


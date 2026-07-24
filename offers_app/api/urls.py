from django.urls import include, path
from rest_framework import routers

from offers_app.api.views import OfferDetailRetrieveView, OfferViewSet


router = routers.SimpleRouter()
router.register(r"offers", OfferViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("offerdetails/<int:pk>/", OfferDetailRetrieveView.as_view(), name="offerdetail-detail"),
]
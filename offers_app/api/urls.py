from django.urls import path, include
from offers_app.api.views import OfferViewSet, OfferDetailRetrieveView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'offers', OfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('offerdetails/<int:pk>/', OfferDetailRetrieveView.as_view(), name='offerdetail-detail')
]
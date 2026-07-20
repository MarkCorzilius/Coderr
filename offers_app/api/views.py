from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

class OfferViewSet(ModelViewSet):
    pass


class OfferDetails(generics.RetrieveAPIView):
    pass
from django.urls import path, include
from rest_framework import routers
from orders_app.api.views import OrderViewSet


router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
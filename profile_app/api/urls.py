from django.urls import path

from profile_app.api.views import (
    BusinessProfilesListAPIView,
    CustomerProfilesListAPIView,
    ProfileRetrieveUpdateAPIView,
)


urlpatterns = [
    path("profile/<int:user_id>/", ProfileRetrieveUpdateAPIView.as_view(), name="profile"),
    path("profiles/business/", BusinessProfilesListAPIView.as_view(), name="profiles-business-list"),
    path("profiles/customer/", CustomerProfilesListAPIView.as_view(), name="profiles-customer-list"),
]
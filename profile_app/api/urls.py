from django.urls import path
from profile_app.api.views import ProfileRetrieveUpdateAPIView

urlpatterns = [
    path('<int:user_id>/', ProfileRetrieveUpdateAPIView.as_view(), name='profile'),
]
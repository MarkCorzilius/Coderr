from django.urls import path
from accounts_app.api.views import RegisterView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
]

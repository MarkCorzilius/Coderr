from django.urls import path
from accounts_app.api.views import RegisterView, LoginView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

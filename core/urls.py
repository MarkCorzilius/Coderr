from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import settings
from core.views import BaseInfoAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("accounts_app.api.urls")),
    path("api/", include("profiles_app.api.urls")),
    path("api/", include("offers_app.api.urls")),
    path("api/", include("orders_app.api.urls")),
    path("api/", include("reviews_app.api.urls")),
    path("api/base-info/", BaseInfoAPIView.as_view(), name="base-info"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

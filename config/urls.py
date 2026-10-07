from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from store.admin import admin_site

urlpatterns = [
    path("quan-tri/", admin_site.urls),
    path("", include("store.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

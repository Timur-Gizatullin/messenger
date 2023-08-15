from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from messenger import settings
from messenger.settings import DEBUG

urlpatterns = [path("admin/", admin.site.urls), path("api/", include("api.urls"))]

if DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

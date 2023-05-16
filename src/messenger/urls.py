from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from messenger.settings import DEBUG

urlpatterns = [path("admin/", admin.site.urls), path("api/", include("api.urls"))]

if DEBUG:
    urlpatterns += staticfiles_urlpatterns()

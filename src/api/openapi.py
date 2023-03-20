from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="I am messenger", default_version="v1", description="i am desc"
    ),
    public=True,
    permission_classes=[AllowAny],
)
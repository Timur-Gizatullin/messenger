from drf_yasg import openapi

limit = openapi.Parameter(
    "limit", openapi.IN_QUERY, description="Number of results to return per page.", type=openapi.TYPE_INTEGER
)
offset = openapi.Parameter(
    "offset",
    openapi.IN_QUERY,
    description="The initial index from which to return the results.",
    type=openapi.TYPE_INTEGER,
)
email = openapi.Parameter("email", openapi.IN_QUERY, description="user's email to find one", type=openapi.TYPE_STRING)

default_limit = 10

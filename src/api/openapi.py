import os
from os.path import abspath

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from plantuml import PlantUML
from rest_framework.permissions import AllowAny

from core import docs_constants


def read_uml(path: str, reference: list[str], server: PlantUML) -> None:
    for file in os.listdir(abspath(path)):
        filename = os.fsdecode(file)
        if filename.endswith(".puml"):
            with open(f"{path}/{filename}") as uml_file:
                reference.append(f"<a href='{server.get_url(uml_file.read())}'>{filename}</a>")


def get_description() -> str:
    result = ["UML diagrams:"]

    server = PlantUML(
        url="http://www.plantuml.com/plantuml/png/",
        basic_auth={},
        form_auth={},
        http_opts={},
        request_opts={},
    )

    read_uml(path=docs_constants.DATA_PIPEPLINE_URL, reference=result, server=server)
    read_uml(path=docs_constants.ER_DIAGRAM_URL, reference=result, server=server)

    return "\n".join(result)


schema_view = get_schema_view(
    openapi.Info(title="I am messenger", default_version="v1", description=get_description()),
    public=True,
    permission_classes=[AllowAny],
)

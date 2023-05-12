import os

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from plantuml import PlantUML
from rest_framework.permissions import AllowAny

from core import docs_constants
from messenger.settings import BASE_DIR


def read_uml_diagrams(path: str, reference: list[str], server: PlantUML) -> None:
    for folder in os.listdir(os.path.join(BASE_DIR, path)):
        for file in os.listdir(os.path.join(BASE_DIR, path, folder)):
            if file.endswith(".puml"):
                with open(os.path.join(BASE_DIR, path, folder, file)) as uml_file:
                    reference.append(f"<a href='{server.get_url(uml_file.read())}'>{file}</a>")


def get_description() -> str:
    result = ["UML diagrams:"]

    server = PlantUML(url=os.environ.get("UML_CONSTRUCTOR_URL", "http://www.plantuml.com/plantuml/png/"))

    read_uml_diagrams(path=docs_constants.DOCS_URL, reference=result, server=server)

    return "\n".join(result)


schema_view = get_schema_view(
    openapi.Info(title="I am messenger", default_version="v1", description=get_description()),
    public=True,
    permission_classes=[AllowAny],
)

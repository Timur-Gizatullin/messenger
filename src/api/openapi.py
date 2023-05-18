import os

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from plantuml import PlantUML
from rest_framework.permissions import AllowAny

from messenger.settings import BASE_DIR, UML_CONSTRUCTOR_URL


def read_uml_diagrams(reference: list[str]) -> None:
    server = PlantUML(url=UML_CONSTRUCTOR_URL)
    path = "../docs"

    for folder in os.listdir(os.path.join(BASE_DIR, path)):
        for file in os.listdir(os.path.join(BASE_DIR, path, folder)):
            if file.endswith(".puml"):
                with open(os.path.join(BASE_DIR, path, folder, file)) as uml_file:
                    reference.append(f"<a href='{server.get_url(uml_file.read())}'>{file}</a>")


def get_description() -> str:
    result = ["UML diagrams:"]

    read_uml_diagrams(reference=result)

    return "\n".join(result)


schema_view = get_schema_view(
    openapi.Info(title="I am messenger", default_version="v1", description=get_description()),
    public=True,
    permission_classes=[AllowAny],
)

import factory

from core.models import User
from tests.factories.mixins import UniqueStringMixin


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = UniqueStringMixin("email")

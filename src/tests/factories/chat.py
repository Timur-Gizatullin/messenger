import factory

from core.models import Chat


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)
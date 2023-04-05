from django.contrib import admin

from core.models import Chat, Message, User
from core.models.attachment import Attachment

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(User)
admin.site.register(Attachment)

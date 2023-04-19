from django.contrib import admin

from core.models import Attachment, Chat, Message, User
from core.models.user_chat import UserChat

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(User)
admin.site.register(Attachment)
admin.site.register(UserChat)

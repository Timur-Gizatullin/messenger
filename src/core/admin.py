from django.contrib import admin

from core.models import Chat, Message, User

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(User)

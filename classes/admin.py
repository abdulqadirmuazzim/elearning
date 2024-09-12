from django.contrib import admin
from .models import Chat


class ChatDisplay(admin.ModelAdmin):
    model = Chat
    list_display = ["sender", "receiver", "time"]


admin.site.register(Chat, ChatDisplay)

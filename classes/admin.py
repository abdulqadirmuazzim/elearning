from django.contrib import admin
from .models import Comment, Chat


class CommentDisplay(admin.ModelAdmin):
    model = Comment
    list_display = ["user", "student", "trainer", "date_commented"]


class ChatDisplay(admin.ModelAdmin):
    model = Chat
    list_display = ["sender", "receiver", "time"]


admin.site.register(Comment, CommentDisplay)
admin.site.register(Chat, ChatDisplay)

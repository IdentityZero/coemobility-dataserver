from django.contrib import admin

from . import models

class ConversationColumns(admin.ModelAdmin):
    list_display = ['creator', 'topic', 'created_at']
admin.site.register(models.Conversation,ConversationColumns)

class MessageColumns(admin.ModelAdmin):
    list_display = ['sender', 'conversation']
admin.site.register(models.Message, MessageColumns)


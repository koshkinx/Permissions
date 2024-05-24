from django.contrib import admin
from .models import Chat, Message


class ChatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('users',)  # Для зручного вибору користувачів


admin.site.register(Chat)
admin.site.register(Message)

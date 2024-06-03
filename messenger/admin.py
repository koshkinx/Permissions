from django.contrib import messages
from .models import Message
from django.contrib import admin
from .models import Chat, Message


# class ChatAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     filter_horizontal = ('users',)  # Для зручного вибору користувачів


# admin.site.register(Chat)
# admin.site.register(Message)


# class MessageAdmin(admin.ModelAdmin):
#     # Определяем дополнительные поля для отображения в списке сообщений
#     list_display = ('sender', 'receiver', 'timestamp')

#     def save_model(self, request, obj, form, change):
#         # Сохраняем модель (сообщение) с помощью стандартного метода сохранения
#         super().save_model(request, obj, form, change)

#         # Проверяем, является ли получатель суперпользователем
#         if obj.receiver.is_superuser:
#             # Если да, отправляем сообщение об успешной отправке сообщения суперпользователю
#             messages.success(
#                 request, "Вы успешно отправили сообщение суперпользователю.")


# # Регистрируем класс представления для модели Message
# admin.site.register(Message, MessageAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'content')

    def save_model(self, request, obj, form, change):
        if not change:  # если это новое сообщение
            if obj.receiver.is_superuser:
                messages.success(
                    request, 'Вы успешно отправили сообщение суперюзеру')
        super().save_model(request, obj, form, change)


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)

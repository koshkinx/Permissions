from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Chat, Message, MessageLog
from .forms import MessageForm
from django.views.generic import View
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib import messages
from .mixins import UppercaseMixin, AddTimestampMixin, PrefixAuthorMixin
from django.shortcuts import render, redirect
from django.contrib import messages
# Класс для детального просмотра сообщений с миксинами для обработки данных


class MessageDetailView(UppercaseMixin, AddTimestampMixin, PrefixAuthorMixin, DetailView):
    model = Message
    template_name = 'message_detail.html'

# Представление для списка чатов пользователя


@login_required  # Требуется аутентификация пользователя
def chat_list(request):
    # Получаем все чаты, в которых состоит пользователь
    chats = request.user.chats.all()
    # Рендерим шаблон с чатами
    return render(request, 'messenger/chat_list.html', {'chats': chats})

# Представление для детального просмотра чата и отправки сообщений


@login_required  # Требуется аутентификация пользователя
def chat_detail(request, chat_id):
    # Получаем чат по ID или возвращаем 404
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.users.all():  # Проверяем, что пользователь состоит в чате
        # Если нет, перенаправляем на список чатов
        return redirect('chat_list')

    if request.method == 'POST':
        # Обрабатываем форму отправки сообщения
        form = MessageForm(request.POST)
        if form.is_valid():
            # Создаем сообщение, но не сохраняем в БД
            message = form.save(commit=False)
            message.chat = chat  # Привязываем сообщение к текущему чату
            message.author = request.user  # Устанавливаем автора сообщения
            message.save()  # Сохраняем сообщение в БД

            # Проверяем, является ли получатель суперпользователем
            if message.chat.users.filter(is_superuser=True).exists():
                # Если да, создаем сообщение о успешной отправке сообщения суперпользователю
                messages.success(
                    request, "Вы успешно отправили сообщение суперпользователю")

            # Перенаправляем на детальный просмотр чата
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()  # Инициализируем пустую форму

    # Рендерим шаблон с чатом и формой
    return render(request, 'messenger/chat_detail.html', {'chat': chat, 'form': form})

# Представление для редактирования сообщений


@login_required  # Требуется аутентификация пользователя
# Проверяем наличие прав на редактирование
@permission_required('messenger.edit_own_message', raise_exception=True)
def edit_message(request, message_id):
    # Получаем сообщение по ID или возвращаем 404
    message = get_object_or_404(Message, id=message_id)
    # Проверяем, что пользователь может редактировать сообщение
    if not message.can_edit(request.user):
        # Если нет, перенаправляем на детальный просмотр чата
        return redirect('chat_detail', chat_id=message.chat.id)

    if request.method == 'POST':
        # Обрабатываем форму редактирования сообщения
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            # Перенаправляем на детальный просмотр чата
            return redirect('chat_detail', chat_id=message.chat.id)
    else:
        # Инициализируем форму с данными сообщения
        form = MessageForm(instance=message)

    # Рендерим шаблон с формой редактирования
    return render(request, 'messenger/edit_message.html', {'form': form})

# Представление для удаления сообщений


@login_required  # Требуется аутентификация пользователя
# Проверяем наличие прав на удаление
@permission_required('messenger.delete_own_message', raise_exception=True)
def delete_message(request, message_id):
    # Получаем сообщение по ID или возвращаем 404
    message = get_object_or_404(Message, id=message_id)
    # Проверяем, что пользователь может удалить сообщение
    if message.can_delete(request.user):
        message.delete()  # Удаляем сообщение
    # Перенаправляем на детальный просмотр чата
    return redirect('chat_detail', chat_id=message.chat.id)


# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.save()
#             messages.success(request, 'Message sent successfully nice!')
#             return redirect('message_success')
#     else:
#         form = MessageForm()
#     return render(request, 'messenger/edit_message.html', {'form': form})


def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('some-view-name')
    else:
        form = MessageForm()
    return render(request, 'messenger/edit_message.html', {'form': form})

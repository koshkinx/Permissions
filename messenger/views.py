from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Chat, Message
from .forms import MessageForm


@login_required
def chat_list(request):
    chats = request.user.chats.all()
    return render(request, 'messenger/chat_list.html', {'chats': chats})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.users.all():
        return redirect('chat_list')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    return render(request, 'messenger/chat_detail.html', {'chat': chat, 'form': form})


@login_required
@permission_required('messenger.edit_own_message', raise_exception=True)
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if not message.can_edit(request.user):
        return redirect('chat_detail', chat_id=message.chat.id)

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_detail', chat_id=message.chat.id)
    else:
        form = MessageForm(instance=message)

    return render(request, 'messenger/edit_message.html', {'form': form})


@login_required
@permission_required('messenger.delete_own_message', raise_exception=True)
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.can_delete(request.user):
        message.delete()
    return redirect('chat_detail', chat_id=message.chat.id)

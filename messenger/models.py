from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Chat(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("edit_own_message", "Can edit own message"),
            ("delete_own_message", "Can delete own message"),
        ]

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'

    def can_edit(self, user):
        return self.author == user and self.created_at > timezone.now() - timedelta(days=1)

    def can_delete(self, user):
        return self.author == user and self.created_at > timezone.now() - timedelta(days=1)

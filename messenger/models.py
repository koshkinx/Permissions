import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .mixins import (
    AddUniqueIdentifierMixin, TrackLastAccessedMixin, TitleCaseNameMixin,
    IncrementalSaveCountMixin, LimitedLengthNameMixin, AutoSlugMixin, AppendSignatureMixin
)


class MessageLog(models.Model):
    sender = models.ForeignKey(
        User, related_name='logs_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='logs_received', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Log: {self.sender} to {self.receiver} at {self.timestamp}'


class Chat(AddUniqueIdentifierMixin, TrackLastAccessedMixin, TitleCaseNameMixin,
           IncrementalSaveCountMixin, LimitedLengthNameMixin, AutoSlugMixin,
           models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='chats')
    last_accessed = models.DateTimeField(null=True, blank=True)
    save_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name='messages_sent', on_delete=models.CASCADE, default=1)
    receiver = models.ForeignKey(
        User, related_name='messages_received', on_delete=models.CASCADE, default=1)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("edit_own_message", "Can edit own message"),
            ("delete_own_message", "Can delete own message"),
        ]

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'

    def _user_has_permission(self, user):
        return self.sender == user and self.timestamp > timezone.now() - timedelta(days=1)

    def can_edit(self, user):
        return self._user_has_permission(user)

    def can_delete(self, user):
        return self._user_has_permission(user)

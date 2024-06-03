# messenger/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Message
import logging
from .models import Message, MessageLog


@receiver(post_save, sender=Message)
def log_message(sender, instance, created, **kwargs):
    if created:
        MessageLog.objects.create(
            sender=instance.sender,
            receiver=instance.receiver,
            content=instance.content
        )

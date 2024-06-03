from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message

        fields = ['sender', 'receiver', 'content']

    def save(self, request, *args, **kwargs):
        instance = super().save(commit=False)
        instance.request = request
        instance.save()
        return instance

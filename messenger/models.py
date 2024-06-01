# from django.db import models  # Импортируем модуль моделей Django
# # Импортируем модель пользователя Django
# from django.contrib.auth.models import User
# # Импортируем модуль для работы с временными зонами
# from django.utils import timezone
# # Импортируем модуль для работы с временными интервалами
# from datetime import timedelta

# # Определяем модель Chat, которая представляет чат


# class Chat(models.Model):
#     # Поле для имени чата, максимальная длина 100 символов
#     name = models.CharField(max_length=100)
#     # Множество пользователей, связанных с чатом
#     users = models.ManyToManyField(User, related_name='chats')

#     def __str__(self):
#         return self.name  # Возвращает имя чата при преобразовании объекта в строку

# # Определяем модель Message, которая представляет сообщение в чате


# class Message(models.Model):
#     chat = models.ForeignKey(
#         # Ссылка на чат, к которому относится сообщение
#         Chat, related_name='messages', on_delete=models.CASCADE)
#     author = models.ForeignKey(
#         User, related_name='messages', on_delete=models.CASCADE)  # Ссылка на автора сообщения
#     content = models.TextField()  # Поле для содержания сообщения
#     # Дата и время создания сообщения
#     created_at = models.DateTimeField(auto_now_add=True)
#     # Дата и время последнего обновления сообщения
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         permissions = [
#             # Право на редактирование собственного сообщения
#             ("edit_own_message", "Can edit own message"),
#             # Право на удаление собственного сообщения
#             ("delete_own_message", "Can delete own message"),
#         ]

#     def __str__(self):
#         # Возвращает первые 20 символов сообщения при преобразовании объекта в строку
#         return f'{self.author.username}: {self.content[:20]}'

#     # Внутренний метод для проверки, может ли пользователь редактировать или удалять сообщение
#     def _user_has_permission(self, user):
#         # Проверяет, является ли пользователь автором сообщения и было ли сообщение создано менее суток назад
#         return self.author == user and self.created_at > timezone.now() - timedelta(days=1)
#     # Метод для проверки, может ли пользователь редактировать сообщение

#     def can_edit(self, user):
#         return self._user_has_permission(user)

#     # Метод для проверки, может ли пользователь удалить сообщение
#     def can_delete(self, user):
#         return self._user_has_permission(user)
# models.py

# from django.db import models  # Импортируем модуль моделей Django
# # Импортируем модель пользователя Django
# from django.contrib.auth.models import User
# # Импортируем модуль для работы с временными зонами
# from django.utils import timezone
# # Импортируем модуль для работы с временными интервалами
# from datetime import timedelta
# from .mixins import (
#     AddUniqueIdentifierMixin, TrackLastAccessedMixin, TitleCaseNameMixin,
#     IncrementalSaveCountMixin, LimitedLengthNameMixin, AutoSlugMixin, AppendSignatureMixin
# )

# # Определяем модель Chat, которая представляет чат


# class Chat(AddUniqueIdentifierMixin, TrackLastAccessedMixin, TitleCaseNameMixin,
#            IncrementalSaveCountMixin, LimitedLengthNameMixin, AutoSlugMixin, models.Model):
#     name = models.CharField(max_length=100)
#     users = models.ManyToManyField(User, related_name='chats')
#     save_count = models.IntegerField(default=0, editable=False)
#     slug = models.SlugField(max_length=100, blank=True)

#     def __str__(self):
#         return self.name  # Возвращает имя чата при преобразовании объекта в строку

# # Определяем модель Message, которая представляет сообщение в чате


# class Message(AppendSignatureMixin, models.Model):
#     chat = models.ForeignKey(
#         Chat, related_name='messages', on_delete=models.CASCADE)
#     author = models.ForeignKey(
#         User, related_name='messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         permissions = [
#             ("edit_own_message", "Can edit own message"),
#             ("delete_own_message", "Can delete own message"),
#         ]

#     def __str__(self):
#         return f'{self.author.username}: {self.content[:20]}'

#     def _user_has_permission(self, user):
#         return self.author == user and self.created_at > timezone.now() - timedelta(days=1)

#     def can_edit(self, user):
#         return self._user_has_permission(user)

#     def can_delete(self, user):
#         return self._user_has_permission(user)


# mixins.py

# models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .mixins import (
    AddUniqueIdentifierMixin, TrackLastAccessedMixin, TitleCaseNameMixin,
    IncrementalSaveCountMixin, LimitedLengthNameMixin, AutoSlugMixin, AppendSignatureMixin
)


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



class Message(AppendSignatureMixin, models.Model):
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

    def _user_has_permission(self, user):
        return self.author == user and self.created_at > timezone.now() - timedelta(days=1)

    def can_edit(self, user):
        return self._user_has_permission(user)

    def can_delete(self, user):
        return self._user_has_permission(user)

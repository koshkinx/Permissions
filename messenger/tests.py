from django.test import TestCase  # Импортируем класс TestCase для написания тестов
# Импортируем модель пользователя Django
from django.contrib.auth.models import User
# Импортируем модуль для работы с временными зонами
from django.utils import timezone
# Импортируем модуль для работы с временными интервалами
from datetime import timedelta
# Импортируем модели Chat и Message из текущего приложения
from .models import Chat, Message


class MessageModelTest(TestCase):

    def setUp(self):
        # Создаем двух пользователей и чат
        self.user1 = User.objects.create_user(
            username='user1', password='pass')
        self.user2 = User.objects.create_user(
            username='user2', password='pass')
        self.chat = Chat.objects.create(name='Test Chat')
        # Добавляем пользователей в чат
        self.chat.users.add(self.user1, self.user2)
        # Создаем сообщение от первого пользователя в чате
        self.message = Message.objects.create(
            chat=self.chat,
            author=self.user1,
            content='This is a test message.',
            created_at=timezone.now()
        )

    def test_user_has_permission(self):
        # Проверяем, что пользователь может редактировать и удалять свое сообщение в течение 1 дня
        self.assertTrue(self.message._user_has_permission(self.user1))
        # Проверяем, что пользователь не может редактировать и удалять свое сообщение после 1 дня
        self.message.created_at = timezone.now() - timedelta(days=2)
        self.assertFalse(self.message._user_has_permission(self.user1))
        # Проверяем, что другой пользователь не может редактировать и удалять сообщение
        self.assertFalse(self.message._user_has_permission(self.user2))

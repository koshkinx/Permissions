import uuid
from django.utils import timezone

# 1. AddUniqueIdentifierMixin: Добавляет уникальный идентификатор к объекту


class AddUniqueIdentifierMixin:
    def save(self, *args, **kwargs):
        if not self.pk:  # Только при создании нового объекта
            self.unique_id = uuid.uuid4()
        super().save(*args, **kwargs)

# 2. TrackLastAccessedMixin: Отслеживает последнее время доступа к объекту


class TrackLastAccessedMixin:
    def save(self, *args, **kwargs):
        self.last_accessed = timezone.now()
        super().save(*args, **kwargs)

# 3. TitleCaseNameMixin: Преобразует имя объекта в заглавный регистр


class TitleCaseNameMixin:
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

# 4. IncrementalSaveCountMixin: Подсчитывает количество сохранений объекта


class IncrementalSaveCountMixin:
    def save(self, *args, **kwargs):
        if not hasattr(self, 'save_count') or self.save_count is None:
            self.save_count = 0
        self.save_count += 1
        super().save(*args, **kwargs)

# 5. LimitedLengthNameMixin: Ограничивает длину имени


class LimitedLengthNameMixin:
    def save(self, *args, **kwargs):
        self.name = self.name[:30]  # Ограничиваем длину имени 30 символами
        super().save(*args, **kwargs)

# 6. AutoSlugMixin: Автоматически генерирует slug из имени


class AutoSlugMixin:
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(' ', '-').lower()
        super().save(*args, **kwargs)

# 7. AppendSignatureMixin: Добавляет подпись к содержимому сообщения


class AppendSignatureMixin:
    def save(self, *args, **kwargs):
        self.content += "\n\n-- This is an automated message."
        super().save(*args, **kwargs)

# внизу 3 миксина с использованием вьюшек


class UppercaseMixin:
    """
    Миксин для преобразования содержимого сообщения в верхний регистр.
    """

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if hasattr(self, 'object'):
            self.object.content = self.object.content.upper()
        return response


class AddTimestampMixin:
    """
    Миксин для добавления временной метки к содержимому сообщения.
    """

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if hasattr(self, 'object'):
            self.object.content += f" (Timestamp: {self.object.created_at})"
        return response


class PrefixAuthorMixin:
    """
    Миксин для добавления префикса с именем автора к содержимому сообщения.
    """

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if hasattr(self, 'object'):
            self.object.content = f"{
                self.object.author.username}: {self.object.content}"
        return response

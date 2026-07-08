"""Модуль модели обратной связи (заявки с главной страницы)."""

from django.db import models


class Feedback(models.Model):
    """
    Заявка, оставленная посетителем через форму на главной странице.

    Attributes:
        name (str): имя отправителя.
        phone (str): контактный телефон.
        email (str | None): email (опционально).
        message (str): текст сообщения / описание задачи.
        created_at (datetime): дата и время создания заявки.
    """

    name = models.CharField(max_length=150, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Заявка от {self.name} ({self.phone})'
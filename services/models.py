"""Модуль каталога услуг компании."""

from django.db import models


class Service(models.Model):
    """
    Услуга, предоставляемая компанией.

    Attributes:
        name (str): название услуги.
        description (str): развёрнутое описание.
        base_price (Decimal): базовая цена за единицу (или за весь объём).
        unit (str | None): единица измерения — «м²», «м.п.», «шт», None если неприменимо.
        is_active (bool): видимость услуги в каталоге.
    """

    name        = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    base_price  = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Базовая цена (руб.)',
    )
    unit        = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Единица измерения',
        help_text='Например: м², м.п., шт. Оставьте пустым, если не применимо.',
    )
    is_active   = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name        = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering            = ['name']

    def __str__(self) -> str:
        unit_str = f' / {self.unit}' if self.unit else ''
        return f'{self.name} — {self.base_price} руб.{unit_str}'
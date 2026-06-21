"""Модуль заказов и калькуляций.

Order -- заголовок заказа (пользователь, итог, статус).
OrderService -- строка заказа: конкретная услуга + её параметры + зафиксированная цена.
"""

from django.conf import settings
from django.db import models


class OrderStatus(models.TextChoices):
    """Перечисление возможных статусов заказа."""

    DRAFT     = 'draft',     'Черновик'
    PAID      = 'paid',      'Оплачен'
    COMPLETED = 'completed', 'Выполнен'
    CANCELLED = 'cancelled', 'Отменён'


class Order(models.Model):
    """Заказ/Калькуляция пользователя.

    Attributes:
        user (FK): владелец заказа.
        status (str): статус из OrderStatus.choices.
        total_price (Decimal): итоговая сумма (пересчитывается через recalculate_total).
        comment (str): произвольный комментарий клиента.
        created_at (datetime): дата создания.
        updated_at (datetime): дата последнего изменения.
    """

    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Пользователь',
    )
    status      = models.CharField(
        max_length=12,
        choices=OrderStatus.choices,
        default=OrderStatus.DRAFT,
        verbose_name='Статус',
    )
    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name='Итоговая цена (руб.)',
    )
    comment     = models.TextField(blank=True, verbose_name='Комментарий')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at  = models.DateTimeField(auto_now=True,     verbose_name='Дата изменения')

    class Meta:
        verbose_name        = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering            = ['-created_at']

    def __str__(self) -> str:
        return f'Заказ #{self.pk} -- {self.user} [{self.get_status_display()}]'

    def recalculate_total(self) -> None:
        """Пересчитывает total_price как сумму line_price всех строк заказа.

        Делает отдельный UPDATE только поля total_price, не затрагивая
        остальные поля и не вызывая полного сохранения модели.
        """
        from django.db.models import Sum
        result = self.items.aggregate(total=Sum('line_price'))['total'] or 0
        self.total_price = result
        self.save(update_fields=['total_price'])


class OrderService(models.Model):
    """Строка заказа: одна услуга с параметрами калькулятора и зафиксированной ценой.

    Цена (unit_price) фиксируется на момент создания строки, поэтому изменение
    прайса в Service не влияет на уже созданные заказы.

    Attributes:
        order (FK): родительский заказ.
        service (FK): выбранная услуга из каталога.
        parameters (JSON): произвольные входные данные калькулятора
            (площадь, высота, материал, коэффициент сложности и т.д.).
        quantity (Decimal): объём / количество единиц.
        unit_price (Decimal): цена за единицу на момент создания строки.
        line_price (Decimal): итог по строке = quantity * unit_price (авто).
    """

    order      = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
    )
    service    = models.ForeignKey(
        'services.Service',
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Услуга',
    )
    parameters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Параметры калькулятора',
    )
    quantity   = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=1,
        verbose_name='Количество',
    )
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена за ед. (руб.)',
    )
    line_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='Сумма по строке (руб.)',
    )

    class Meta:
        verbose_name        = 'Строка заказа'
        verbose_name_plural = 'Строки заказа'

    def save(self, *args, **kwargs):
        """Автоматически вычисляет line_price = quantity * unit_price перед сохранением."""
        self.line_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.service.name} x {self.quantity} = {self.line_price} руб.'
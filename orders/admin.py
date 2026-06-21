"""Регистрация моделей Order и OrderService в административной панели."""

from django.contrib import admin

from .models import Order, OrderService


class OrderServiceInline(admin.TabularInline):
    """Встроенная таблица строк заказа внутри страницы заказа."""

    model          = OrderService
    extra          = 1
    readonly_fields = ('line_price',)
    fields         = ('service', 'quantity', 'unit_price', 'line_price', 'parameters')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Административный интерфейс для заказов с инлайн-строками."""

    list_display   = ('pk', 'user', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter    = ('status',)
    search_fields  = ('user__email', 'user__first_name', 'comment')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    ordering       = ('-created_at',)
    inlines        = [OrderServiceInline]

    actions = ['recalculate_totals']

    @admin.action(description='Пересчитать итоговые суммы выбранных заказов')
    def recalculate_totals(self, request, queryset):
        """Действие: пересчитывает total_price для выбранных заказов."""
        for order in queryset:
            order.recalculate_total()
        self.message_user(request, f'Пересчитано заказов: {queryset.count()}')


@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    """Административный интерфейс для строк заказа (для прямого просмотра)."""

    list_display  = ('pk', 'order', 'service', 'quantity', 'unit_price', 'line_price')
    search_fields = ('order__pk', 'service__name')
    readonly_fields = ('line_price',)
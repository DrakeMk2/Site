"""Регистрация модели Service в административной панели."""

from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Административный интерфейс для каталога услуг."""

    list_display   = ('name', 'base_price', 'unit', 'is_active')
    list_filter    = ('is_active',)
    search_fields  = ('name', 'description')
    list_editable  = ('is_active',)
    ordering       = ('name',)
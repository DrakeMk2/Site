"""Регистрация модели User в административной панели."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Административный интерфейс для кастомного пользователя с логином по email."""

    ordering         = ['-date_joined']
    list_display     = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter      = ('role', 'is_active', 'is_staff')
    search_fields    = ('email', 'first_name', 'last_name')
    readonly_fields  = ('date_joined', 'last_login')

    # Переопределяем fieldsets под email-логин (убираем username)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Личные данные'), {'fields': ('first_name', 'last_name', 'role')}),
        (_('Права доступа'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    # Форма создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_active'),
        }),
    )
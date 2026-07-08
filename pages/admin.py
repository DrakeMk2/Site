from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Админ-панель для заявок с главной страницы."""

    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
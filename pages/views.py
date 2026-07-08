"""Представления приложения pages: главная страница и страницы-заглушки."""

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Feedback


def home_view(request):
    """
    Главная страница сайта.

    GET  — рендерит страницу с пустой формой.
    POST — валидирует данные формы, сохраняет заявку Feedback,
           добавляет flash-сообщение и редиректит на главную.

    Returns:
        HttpResponse: отрендеренный шаблон home.html или редирект.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()

        # Простейшая серверная валидация обязательных полей
        errors = []
        if not name:
            errors.append('Имя обязательно для заполнения.')
        if not phone:
            errors.append('Телефон обязателен для заполнения.')
        if not message_text:
            errors.append('Сообщение обязательно для заполнения.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'pages/home.html')

        Feedback.objects.create(
            name=name,
            phone=phone,
            email=email or '',
            message=message_text,
        )
        messages.success(request, 'Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время.')
        return redirect('home')

    return render(request, 'pages/home.html')


def services_stub_view(request):
    """
    Страница-заглушка для каталога услуг.

    Returns:
        HttpResponse: шаблон services.html с сообщением о разработке.
    """
    return render(request, 'pages/stub.html', {
        'title': 'Услуги',
        'message': 'Каталог услуг находится в разработке.',
    })


def calculator_stub_view(request):
    """
    Страница-заглушка для калькулятора.

    Returns:
        HttpResponse: шаблон calculator.html с сообщением о разработке.
    """
    return render(request, 'pages/stub.html', {
        'title': 'Калькулятор',
        'message': 'Калькулятор стоимости находится в разработке.',
    })
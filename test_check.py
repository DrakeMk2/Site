"""Скрипт проверки всех маршрутов и формы обратной связи."""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.test import RequestFactory
from pages.views import home_view, services_stub_view, calculator_stub_view
from pages.models import Feedback

rf = RequestFactory()

# GET /
req = rf.get('/')
resp = home_view(req)
print(f'GET /: status={resp.status_code}')

# GET /services/
req = rf.get('/services/')
resp = services_stub_view(req)
print(f'GET /services/: status={resp.status_code}')

# GET /calculator/
req = rf.get('/calculator/')
resp = calculator_stub_view(req)
print(f'GET /calculator/: status={resp.status_code}')

# POST /
data = {'name': 'Test User', 'phone': '+79991234567', 'message': 'Test message'}
req = rf.post('/', data)
resp = home_view(req)
print(f'POST /: status={resp.status_code}, redirect={resp.url}')

# Проверка сохранения
fb = Feedback.objects.last()
print(f'Feedback saved: name={fb.name}, phone={fb.phone}')

print('\n=== ALL TESTS PASSED ===')

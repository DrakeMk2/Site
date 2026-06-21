"""Базовые тесты моделей: User, Service, Order, OrderService."""

from decimal import Decimal

from django.test import TestCase

from services.models import Service
from users.models import User, UserRole

from .models import Order, OrderService, OrderStatus


class UserModelTest(TestCase):
    """Тесты кастомной модели пользователя."""

    def test_create_user_sets_email_and_hashes_password(self):
        """create_user сохраняет email и хеширует пароль."""
        user = User.objects.create_user(
            email='client@example.com',
            password='secret123',
            first_name='Иван',
        )
        self.assertEqual(user.email, 'client@example.com')
        self.assertTrue(user.check_password('secret123'))

    def test_new_user_is_inactive_by_default(self):
        """Новый пользователь неактивен по умолчанию."""
        user = User.objects.create_user(
            email='inactive@example.com',
            password='pass',
            first_name='Анна',
        )
        self.assertFalse(user.is_active)

    def test_new_user_has_client_role_by_default(self):
        """Роль по умолчанию — CLIENT."""
        user = User.objects.create_user(
            email='role@example.com',
            password='pass',
            first_name='Пётр',
        )
        self.assertEqual(user.role, UserRole.CLIENT)

    def test_create_superuser_is_active_staff_superuser(self):
        """create_superuser создаёт активного суперпользователя."""
        su = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass',
            first_name='Админ',
        )
        self.assertTrue(su.is_active)
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)
        self.assertEqual(su.role, UserRole.ADMIN)

    def test_full_name_property(self):
        """Свойство full_name возвращает имя и фамилию через пробел."""
        user = User.objects.create_user(
            email='fn@example.com',
            password='pass',
            first_name='Иван',
            last_name='Иванов',
        )
        self.assertEqual(user.full_name, 'Иван Иванов')

    def test_str_representation(self):
        """__str__ возвращает имя и email в угловых скобках."""
        user = User.objects.create_user(
            email='str@example.com',
            password='pass',
            first_name='Мария',
        )
        self.assertIn('str@example.com', str(user))


class ServiceModelTest(TestCase):
    """Тесты модели Service."""

    def setUp(self):
        self.service = Service.objects.create(
            name='Штукатурка стен',
            base_price=Decimal('350.00'),
            unit='м2',
        )

    def test_service_str_includes_name_and_price(self):
        """__str__ содержит название и цену."""
        result = str(self.service)
        self.assertIn('Штукатурка стен', result)
        self.assertIn('350', result)

    def test_service_is_active_by_default(self):
        """Новая услуга активна по умолчанию."""
        self.assertTrue(self.service.is_active)


class OrderModelTest(TestCase):
    """Тесты моделей Order и OrderService."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='order_user@example.com',
            password='pass',
            first_name='Клиент',
        )
        self.service = Service.objects.create(
            name='Покраска',
            base_price=Decimal('200.00'),
            unit='м2',
        )
        self.order = Order.objects.create(user=self.user)

    def test_order_default_status_is_draft(self):
        """Статус нового заказа — черновик."""
        self.assertEqual(self.order.status, OrderStatus.DRAFT)

    def test_order_default_total_price_is_zero(self):
        """Начальный total_price равен нулю."""
        self.assertEqual(self.order.total_price, Decimal('0'))

    def test_order_service_calculates_line_price_on_save(self):
        """OrderService.save() автоматически вычисляет line_price."""
        item = OrderService.objects.create(
            order=self.order,
            service=self.service,
            quantity=Decimal('10.000'),
            unit_price=Decimal('200.00'),
            parameters={'area': 10, 'material': 'акриловая'},
        )
        self.assertEqual(item.line_price, Decimal('2000.00'))

    def test_recalculate_total_sums_all_items(self):
        """recalculate_total() суммирует line_price всех строк заказа."""
        OrderService.objects.create(
            order=self.order,
            service=self.service,
            quantity=Decimal('5.000'),
            unit_price=Decimal('200.00'),
        )
        OrderService.objects.create(
            order=self.order,
            service=self.service,
            quantity=Decimal('3.000'),
            unit_price=Decimal('200.00'),
        )
        self.order.recalculate_total()
        self.order.refresh_from_db()
        # 5*200 + 3*200 = 1000 + 600 = 1600
        self.assertEqual(self.order.total_price, Decimal('1600.00'))

    def test_order_str_contains_pk_and_status(self):
        """__str__ заказа содержит pk и статус."""
        result = str(self.order)
        self.assertIn(str(self.order.pk), result)
        self.assertIn('Черновик', result)
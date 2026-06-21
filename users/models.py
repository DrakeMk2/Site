"""Модуль кастомной модели пользователя. Логин выполняется по email."""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserRole(models.TextChoices):
    """Перечисление ролей пользователя."""

    CLIENT = 'client', 'Клиент'
    ADMIN  = 'admin',  'Администратор'


class UserManager(BaseUserManager):
    """Менеджер для создания пользователей и суперпользователей."""

    def create_user(self, email: str, password: str = None, **extra_fields):
        """
        Создаёт и сохраняет обычного пользователя.

        Args:
            email: адрес электронной почты (используется как логин).
            password: пароль в открытом виде (будет захеширован).
            **extra_fields: дополнительные поля модели.

        Returns:
            User: сохранённый экземпляр пользователя.
        """
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # хеширует через Django PBKDF2
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Создаёт суперпользователя с правами администратора.

        Args:
            email: адрес электронной почты.
            password: пароль в открытом виде.
            **extra_fields: дополнительные поля модели.

        Returns:
            User: сохранённый суперпользователь.
        """
        extra_fields.setdefault('role', UserRole.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомный пользователь. Идентификатор — email.

    Attributes:
        email (str): уникальный адрес, используется для входа.
        first_name (str): имя пользователя.
        last_name (str): фамилия пользователя (необязательно).
        role (str): роль из UserRole.choices.
        is_active (bool): флаг активации аккаунта (email-подтверждение).
        is_staff (bool): доступ к /admin/.
        date_joined (datetime): дата регистрации, проставляется автоматически.
    """

    email       = models.EmailField(unique=True, verbose_name='Email')
    first_name  = models.CharField(max_length=100, verbose_name='Имя')
    last_name   = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    role        = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CLIENT,
        verbose_name='Роль',
    )
    is_active   = models.BooleanField(default=False, verbose_name='Активирован')
    is_staff    = models.BooleanField(default=False, verbose_name='Персонал')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    class Meta:
        verbose_name        = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering            = ['-date_joined']

    def __str__(self) -> str:
        return f'{self.first_name} <{self.email}>'

    @property
    def full_name(self) -> str:
        """Возвращает полное имя пользователя."""
        return f'{self.first_name} {self.last_name}'.strip()
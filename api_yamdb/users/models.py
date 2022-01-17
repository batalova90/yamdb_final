from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
]


class User(AbstractUser):
    """Add additional fields to User model."""
    bio = models.TextField(
        'Biography',
        blank=True
    )
    role = models.CharField(
        'Role',
        blank=True,
        max_length=30,
        choices=USER_ROLES,
        default='user'
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

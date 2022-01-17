from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Register User's model in Admin section."""
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'bio', 'role')
    empty_value_display = '-пусто-'

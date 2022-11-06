from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Информация о пользователе', {'fields': ('first_name', 'last_name', 'organization')}),
        ('Контактные данные', {'fields': ('phone', 'email', 'telegram')}),
        ('Рассылка', {'fields': ('subscribe_mail', 'subscribe_telegram',)}),
        ('Роли', {'fields': ('is_operator', 'is_assistant',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(Room)
admin.site.register(Server)
admin.site.register(Application)
admin.site.register(Grade)

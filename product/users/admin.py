from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import Balance, CustomUser, Subscription

admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомного пользователя."""

    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    )
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {
         'fields': ('first_name', 'last_name', 'username')}),
        ('Права доступа', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
        )}
        ),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'username',
                'password1',
                'password2'
            ),
        }),
    )


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    """Админка для баланса пользователя."""

    list_display = ('user', 'bonuses')
    list_filter = ('user',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

    fieldsets = (
        (None, {
            'fields': ('user', 'bonuses')
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка для подписок на курсы."""

    list_display = ('user', 'course')
    list_filter = ('course', 'user')
    search_fields = ('user__email', 'course__title')

    fieldsets = (
        (None, {
            'fields': ('user', 'course')
        }),
    )

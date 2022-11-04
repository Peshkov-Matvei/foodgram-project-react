from django.contrib import admin

from .models import Subscribe, User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
    )
    list_filter = (
        'first_name',
        'email',
    )
    empty_value_display = '-пусто-'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'

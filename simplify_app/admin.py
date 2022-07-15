from django.contrib import admin

from simplify_app.models import User, SimpleUrl


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (
        ('username', 'email'),
        ('first_name', 'last_name'),
        ('send_messages', 'is_active', 'is_activated'),
        ('is_staff', 'is_superuser'),
        'groups', 'user_permissions',
        ('last_login', 'date_joined')
    )
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(User, UserAdmin)


class SimpleUrlAdmin(admin.ModelAdmin):
    list_display = ('simple_url_id', 'original_url', 'user', 'created_at')


admin.site.register(SimpleUrl, SimpleUrlAdmin)

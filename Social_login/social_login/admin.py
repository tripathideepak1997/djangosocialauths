from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from social_login.models import User


class UserAdminPanel(UserAdmin):
    model = User
    list_display = ('first_name', 'last_name', 'username', 'email')
    list_filter = ('first_name', 'email')
    search_fields = ['first_name', 'email', 'username']
    readonly_fields = ('image_tag',)

    fieldsets = (
        (None, {
            'fields': (('first_name', 'last_name', 'gender'),
                       ('username',))
        }),
        (None, {
            'fields': (('is_staff', 'is_active'),)
        }),
        (None, {
            'fields': (('phone_number', 'date_joined',), ('profile_photo', 'image_tag',))
        }),
    )


admin.site.register(User, UserAdminPanel)

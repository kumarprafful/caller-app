from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('mobile', 'full_name', 'email', 'password',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Contacts'), {'fields': ('contacts',)}),
        (_('Important date'), {'fields': ('last_login', 'date_joined', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2', 'email', 'full_name','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined'),
        }),
    )
    list_display = ('mobile', 'full_name', 'email', 'date_joined',)
    search_fields = ('email', 'mobile', 'full_name',)
    filter_horizontal = ('contacts',)
    ordering = ('-date_joined',)

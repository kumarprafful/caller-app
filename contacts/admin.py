from django.contrib import admin

from contacts.models import Contact, Spam


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'mobile']
    search_fields = ['full_name', 'mobile']
    ordering = ['-created_on']

admin.site.register(Spam)

from django.contrib import admin

from .models import SiteSetting


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value', 'is_active')
    list_filter = ('is_active',)
    ordering = ('id',)
    search_fields = ('key',)


admin.site.register(SiteSetting, SiteSettingAdmin)

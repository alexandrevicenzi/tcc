from django.contrib import admin

from .models import SiteSetting


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'is_active')
    ordering = ('id',)


admin.site.register(SiteSetting, SiteSettingAdmin)

from django.contrib import admin

from .models import AccessToken


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'access_key', 'is_active')
    ordering = ('id',)


admin.site.register(AccessToken, AccessTokenAdmin)

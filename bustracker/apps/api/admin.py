from django.contrib import admin

from .models import AccessToken


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'access_key', 'is_active')
    list_filter = ('is_active',)
    ordering = ('id',)
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'user__email')


admin.site.register(AccessToken, AccessTokenAdmin)

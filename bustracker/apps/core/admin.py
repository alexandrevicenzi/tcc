from django.contrib import admin

from .models import Bus, BusRoute, BusTerminal


class BusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    ordering = ('id',)
    raw_id_fields = ('route',)
    search_fields = ('name',)


class BusRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'is_active')
    list_filter = ('is_active',)
    ordering = ('id',)
    raw_id_fields = ('from_terminal', 'to_terminal', 'terminals')
    search_fields = ('name', 'code')


class BusTerminalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    ordering = ('id',)
    search_fields = ('name',)


admin.site.register(Bus, BusAdmin)
admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(BusTerminal, BusTerminalAdmin)

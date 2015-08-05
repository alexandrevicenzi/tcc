from django.contrib import admin

from .models import Bus, BusRoute, BusTerminal


class BusAdmin(admin.ModelAdmin):
    ordering = ('id',)


class BusRouteAdmin(admin.ModelAdmin):
    ordering = ('id',)


class BusTerminalAdmin(admin.ModelAdmin):
    ordering = ('id',)


admin.site.register(Bus, BusAdmin)
admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(BusTerminal, BusTerminalAdmin)

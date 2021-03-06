from django.contrib import admin

from .models import AccessPoint, Bus, BusRoute, BusStop


class AccessPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'ssid', 'bssid', 'is_active')
    list_filter = ('is_active',)
    ordering = ('id',)


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
    raw_id_fields = ('from_stop', 'to_stop', 'stops')
    search_fields = ('name', 'code')


class BusStopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    ordering = ('id',)
    raw_id_fields = ('aps',)
    search_fields = ('name',)


admin.site.register(AccessPoint, AccessPointAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(BusStop, BusStopAdmin)

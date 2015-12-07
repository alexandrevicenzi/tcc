from django.db.models import Q
from django.shortcuts import render

from apps.core.models import BusStop, Bus


def index(request):
    return render(request, 'site/index.html', {})


def about(request):
    return render(request, 'site/about.html', {})


def bus_stations(request):
    def can_list(bus, station, start, end):
        if bus and station:
            time = bus.estimated_arrival_to(station.latitude, station.longitude)
            if time:
                return start <= time.minutes <= end
        return False

    stop_id = request.GET.get('id')
    station = None
    bus_list = []

    station_list = BusStop.objects.filter(is_active=True, stop_type='bus-station')

    if stop_id:
        stop_id = int(stop_id)

        try:
            station = BusStop.objects.get(pk=stop_id)
        except BusStop.DoesNotExist:
            pass

        bus_list = Bus.objects.filter(Q(route__to_stop__pk=stop_id) | Q(route__stops__pk=stop_id), is_active=True)
        bus_list = set(bus_list)

    return render(request, 'site/bus_stations.html', {
        'station_list': [s.to_dict() for s in station_list],  # sorted([s.to_dict() for s in station_list], key=lambda t: s['name']),
        'station': station,
        'bus_list': filter(lambda bus: can_list(bus, station, 0, 15), bus_list),
        'bus_list_15': filter(lambda bus: can_list(bus, station, 16, 30), bus_list),
        'bus_list_30': filter(lambda bus: can_list(bus, station, 31, 45), bus_list),
        'bus_list_45': filter(lambda bus: can_list(bus, station, 46, 99999), bus_list),
    })


def bus_map(request):
    return render(request, 'site/bus_map.html', {})


def bus_route(request):
    bus_id = request.GET.get('id')
    bus = None

    if bus_id:
        try:
            bus = Bus.objects.get(is_active=True, pk=bus_id)
        except Bus.DoesNotExist:
            pass

    bus_list = Bus.objects.filter(is_active=True)

    return render(request, 'site/bus_route.html', {
        'bus': bus,
        'bus_list': bus_list,
    })

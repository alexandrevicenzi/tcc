from django.shortcuts import render

from apps.core.models import BusStop, Bus


def index(request):
    return render(request, 'site/index.html', {})


def about(request):
    return render(request, 'site/about.html', {})


def bus_stations(request):
    l = list(BusStop.objects.filter(is_active=True, stop_type='bus-station'))
    return render(request, 'site/bus_stations.html', {
        'station_list': sorted([t.to_dict() for t in l], key=lambda t: t['name'])
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
    return render(request, 'site/bus_route.html', {'bus': bus, 'bus_list': bus_list})

from django.shortcuts import render

from apps.core.models import BusTerminal


def index(request):
    return render(request, 'site/index.html', {
        'terminal_list': sorted([t.to_dict() for t in list(BusTerminal.objects.filter(is_active=True))], key=lambda t: t['name'])
        })


def bus_map(request):
    return render(request, 'site/bus_map.html', {})

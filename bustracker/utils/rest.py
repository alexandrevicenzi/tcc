# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from functools import wraps

from apps.api.models import AccessToken


def json_response(view):
    def _wrap(request, *args, **kwargs):
        value = view(request, *args, **kwargs)
        if isinstance(value, HttpResponse):
            return value
        try:
            return HttpResponse(json.dumps(value), content_type="application/json")
        except Exception as e:
            error = {
                'message': str(e),
                'type': e.__class__.__name__
            }
            return HttpResponse(json.dumps(error), status=500, content_type="application/json")
    return _wrap


def token_auth(view):
    @wraps(view)
    def _decorator(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            authmeth, token = request.META['HTTP_AUTHORIZATION'].split(' ', 1)

            if authmeth.lower() == 'token':
                try:
                    act = AccessToken.objects.get(access_key=token, is_active=True)
                    user = act.user
                except AccessToken.DoesNotExist:
                    user = None

                if user:
                    request.user = user

        if request.user.is_authenticated():
            return view(request, *args, **kwargs)
        else:
            response = HttpResponse('Unauthorized', status=401)
            response['WWW-Authenticate'] = 'Token'
            return response

    return _decorator


def allow_methods(methods):
    def _wrap(view):
        def wrapped_view(request, *args, **kwargs):
            if not request.method in methods:
                return HttpResponse(status=405)
            return view(request, *args, **kwargs)
        wrapped_view.csrf_exempt = True
        return wrapped_view
    return _wrap

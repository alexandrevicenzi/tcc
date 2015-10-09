# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from functools import wraps

from .models import AccessToken


def json_response(fn):
    def _wrap(request, *args, **kwargs):
        value = fn(request, *args, **kwargs)
        return HttpResponse(json.dumps(value), content_type="application/json")
    return _wrap


def token_auth(func):
    @wraps(func)
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
            return func(request, *args, **kwargs)
        else:
            response = HttpResponse('Unauthorized', status=401)
            response['WWW-Authenticate'] = 'Token'
            return response

    return _decorator


@token_auth
@json_response
def index(request):
    return 'Bem Vindo %s!' % request.user.username

from django.http import HttpResponse


class CustomExceptionMiddleware:
    def process_exception(self, request, exception):
        if exception.__class__.__name__ == 'SettingNameNotFound':
            return HttpResponse(str(exception), content_type="text/plain")

        if exception.__class__.__name__ == 'Api404':
            return HttpResponse(status=404)

        raise exception

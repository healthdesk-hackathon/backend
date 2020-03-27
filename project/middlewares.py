from django.http import HttpResponse


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'X-HealthCheck' in request.headers:
            return HttpResponse('OK', content_type='text/plain')
        return self.get_response(request)

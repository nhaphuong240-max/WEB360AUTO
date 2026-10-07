from django.shortcuts import redirect
from django.utils import timezone

from .models import PathRedirect
from .services import release_expired


class ReleaseExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        release_expired()
        try:
            from .phase3 import send_due_reminders
            send_due_reminders()
        except Exception:
            pass
        return self.get_response(request)


class LegacyRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code != 404:
            return response
        rule = PathRedirect.objects.filter(old_path=request.path, until__gte=timezone.localdate()).first()
        if rule:
            return redirect(rule.new_path)
        return response

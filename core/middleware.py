
from django.db import DatabaseError
from django.utils import timezone

from .models import VisitorLog


class VisitorLoggingMiddleware:
    """
    Record public GET page visits.
    Do not record Django admin, static files, or media files.
    """

    EXCLUDED_PREFIXES = (
        "/admin/",
        "/static/",
        "/media/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method != "GET":
            return response

        if any(
            request.path.startswith(prefix)
            for prefix in self.EXCLUDED_PREFIXES
        ):
            return response

        if response.status_code >= 400:
            return response

        # Use the direct connection address. Do not trust
        # forwarded-IP headers unless a trusted proxy is configured.
        ip_address = request.META.get("REMOTE_ADDR")

        if not ip_address:
            return response

        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

        try:
            VisitorLog.objects.create(
                ip_address=ip_address,
                path=request.get_full_path()[:500],
                visited_at=timezone.now(),
                user_agent=user_agent,
            )
        except (DatabaseError, ValueError):
            # Logging failure should not prevent the page loading.
            pass

        return response

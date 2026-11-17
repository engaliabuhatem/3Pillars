"""Admin hardening: login throttling and optional mandatory TOTP for staff."""

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def client_ip(request) -> str:
    """
    The visitor's address. X-Real-IP is only trusted when NUM_PROXIES says a
    proxy (nginx) sets it; otherwise anyone could send the header themselves
    and dodge the login lockout.
    """
    if settings.REST_FRAMEWORK.get("NUM_PROXIES"):
        return request.META.get("HTTP_X_REAL_IP") or request.META.get("REMOTE_ADDR", "")
    return request.META.get("REMOTE_ADDR", "")


class AdminLoginThrottleMiddleware:
    """
    Locks an IP out of the admin login after repeated failures.

    A failure is a POST to the login URL that does not end in a redirect (the
    admin re-renders the form on a bad password).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != "POST" or request.path != reverse("admin:login"):
            return self.get_response(request)

        key = f"admin-login-fail:{client_ip(request)}"
        if cache.get(key, 0) >= settings.ADMIN_LOGIN_ATTEMPTS:
            return HttpResponse(
                "Too many sign-in attempts. Please wait 15 minutes and try again.",
                status=429,
                content_type="text/plain",
            )

        response = self.get_response(request)
        if response.status_code == 302:
            cache.delete(key)
        else:
            cache.set(key, cache.get(key, 0) + 1, settings.ADMIN_LOGIN_LOCKOUT_SECONDS)
        return response


class AdminTwoFactorMiddleware:
    """
    With ADMIN_REQUIRE_2FA on, a signed-in staff member must also have passed
    a TOTP check (django-otp) before any admin page other than the
    verification page itself.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.ADMIN_REQUIRE_2FA and self._needs_verification(request):
            return redirect(f"{reverse('admin-verify-otp')}?next={request.get_full_path()}")
        return self.get_response(request)

    @staticmethod
    def _needs_verification(request) -> bool:
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated or not request.path.startswith(reverse("admin:index")):
            return False
        exempt = {reverse("admin:login"), reverse("admin:logout"), reverse("admin-verify-otp")}
        return request.path not in exempt and not user.is_verified()

"""
    /admin/   the 3 Pillars CMS, themed by adminkit
    /api/     the content API the Next.js site consumes
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.otp_views import verify_otp

admin.site.site_header = "3 Pillars"

urlpatterns = [
    path("admin/verify/", verify_otp, name="admin-verify-otp"),
    path("admin/", admin.site.urls),
    path("api/", include("config.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

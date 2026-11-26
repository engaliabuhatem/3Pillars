"""
Django settings for the 3 Pillars CMS.

Two audiences:
  * the 3 Pillars team, through the admin (themed by `adminkit`)
  * the Next.js site, through the read-only JSON API at /api

Configuration comes from the environment; see `.env.example`.
"""

from pathlib import Path

import environ
from django.templatetags.static import static

from adminkit.nav import dashboard_item, group, item
from adminkit.theme import build_unfold

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    CORS_ALLOWED_ORIGINS=(list, ["http://localhost:3000"]),
    CSRF_TRUSTED_ORIGINS=(list, []),
    SECURE_SSL_REDIRECT=(bool, False),
    ADMIN_REQUIRE_2FA=(bool, False),
    NOTIFY_FROM_EMAIL=(str, "3 Pillars <no-reply@localhost>"),
)
environ.Env.read_env(BASE_DIR / ".env")

# ── Core ─────────────────────────────────────────────────────────────────
_DEV_KEY = "dev-only-insecure-key-change-me"
SECRET_KEY = env("SECRET_KEY", default=_DEV_KEY)
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

if not DEBUG and SECRET_KEY == _DEV_KEY:
    raise RuntimeError(
        "SECRET_KEY must be set when DEBUG=False. Generate one with: "
        "python -c \"from django.core.management.utils import "
        'get_random_secret_key; print(get_random_secret_key())"'
    )

# ── Applications ─────────────────────────────────────────────────────────
# Order is load-bearing (adminkit/README.md §3): adminkit before unfold so its
# dashboard template wins; unfold before django.contrib.admin.
INSTALLED_APPS = [
    "adminkit",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "apps.core",
    "apps.content",
    "apps.bd",
    "apps.careers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "apps.core.security.AdminLoginThrottleMiddleware",
    "apps.core.security.AdminTwoFactorMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ── Database ─────────────────────────────────────────────────────────────
DATABASES = {
    "default": env.db_url("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

# Shared by every worker: the admin login lockout and the form throttle count
# here, so production uses a file (or Redis) cache, not per-process memory.
CACHES = {"default": env.cache_url("CACHE_URL", default="locmemcache://3pillars")}

LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "admin:index"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── Internationalisation ─────────────────────────────────────────────────
# Arabic content lives in `_ar` columns: it is editor-entered content, not
# interface strings, so Django's gettext machinery is not involved.
LANGUAGE_CODE = "en-gb"
LANGUAGES = [("en", "English"), ("ar", "Arabic")]
TIME_ZONE = "Asia/Aden"
USE_I18N = True
USE_TZ = True

# ── Static, media and private files ──────────────────────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/assets/"
MEDIA_ROOT = Path(env("MEDIA_ROOT", default=str(BASE_DIR / "assets")))

# CVs and RFP attachments. Never under MEDIA_ROOT, never given a URL: staff
# download them through an authenticated admin view only.
PRIVATE_MEDIA_ROOT = Path(env("PRIVATE_MEDIA_ROOT", default=str(BASE_DIR / "private")))

DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Security ─────────────────────────────────────────────────────────────
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

# Staff TOTP. Off by default so the first superuser can log in and enrol a
# device; switch on once every staff account has one.
ADMIN_REQUIRE_2FA = env("ADMIN_REQUIRE_2FA")
ADMIN_LOGIN_ATTEMPTS = 5
ADMIN_LOGIN_LOCKOUT_SECONDS = 15 * 60

# Cloudflare Turnstile. Enabled per site in Site settings; the secret is env.
TURNSTILE_SECRET_KEY = env("TURNSTILE_SECRET_KEY", default="")

# ── Revalidation webhook ─────────────────────────────────────────────────
# Every content save tells Next.js which cache tags to drop. The body is
# HMAC-SHA256 signed with the shared secret; Next rejects anything unsigned.
# The site serves every address with a trailing slash; a POST to the other form would be redirected and lost.
REVALIDATE_URL = env("REVALIDATE_URL", default="")
if REVALIDATE_URL and not REVALIDATE_URL.endswith("/"):
    REVALIDATE_URL += "/"
REVALIDATE_SECRET = env("REVALIDATE_SECRET", default="")

# ── Email ────────────────────────────────────────────────────────────────
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend"
    if DEBUG else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env("NOTIFY_FROM_EMAIL")

# ── API ──────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")
SITE_URL = env("SITE_URL", default="http://localhost:3000")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": ["apps.core.wire.CamelCaseJSONRenderer"],
    "DEFAULT_PARSER_CLASSES": [
        "apps.core.wire.CamelCaseJSONParser",
        "apps.core.wire.CamelCaseMultiPartParser",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "apps.core.wire.Pagination",
    "PAGE_SIZE": 24,
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"anon": "600/min", "forms": env("FORM_THROTTLE_RATE", default="10/hour")},
    "UNAUTHENTICATED_USER": None,
    # Behind nginx (production) the client IP is the last X-Forwarded-For hop.
    # 0 = no proxy: use the socket address, never a client-supplied header.
    "NUM_PROXIES": env.int("NUM_PROXIES", default=0),
}

# ── Admin (adminkit) ─────────────────────────────────────────────────────
# Models are "app_label.ModelName" strings: settings load before the app
# registry, so importing a model here would raise AppRegistryNotReady.
ADMIN_NAVIGATION = [
    group("Overview", [dashboard_item()]),
    group("Business development", [
        item("bd.ProposalRequest", "Consultation requests", icon="request_quote"),
        item("bd.Enquiry", "Enquiries", icon="inbox"),
        item("bd.DownloadLead", "Download leads", icon="download"),
        item("content.Client", "Clients & partners", icon="handshake"),
    ]),
    group("Website — Home", [
        item("core.HomeSection", "Home sections", icon="view_agenda"),
        item("content.Pillar", "The three pillars", icon="view_column"),
        item("content.ValuePoint", "Value points", icon="star"),
        item("content.KPI", "Key figures", icon="monitoring"),
        item("content.Testimonial", "Testimonials", icon="format_quote"),
    ]),
    group("Website — About", [
        item("content.CompanyValue", "Values", icon="diamond"),
        item("content.ApproachStep", "Approach steps", icon="timeline"),
        item("content.TeamMember", "Leadership & team", icon="groups"),
    ]),
    group("Website — Content", [
        item("content.Service", "Services", icon="engineering"),
        item("content.Sector", "Sectors", icon="category"),
        item("content.Project", "Projects", icon="apartment"),
        item("core.Page", "Pages", icon="description"),
        item("content.Office", "Offices", icon="location_on"),
        item("content.Certification", "Certifications", icon="verified"),
        item("content.Download", "Downloads", icon="picture_as_pdf"),
    ]),
    group("Website — Insights", [
        item("content.Insight", "Insights", icon="article"),
        item("content.InsightCategory", "Categories", icon="label"),
    ]),
    group("Careers", [
        item("careers.Job", "Jobs", icon="work"),
        item("careers.Application", "Applications", icon="assignment_ind"),
    ]),
    group("Configuration", [
        item("core.SiteSettings", "Site settings", icon="tune"),
        item("core.LaunchReadiness", "Launch readiness", icon="rocket_launch"),
        item("core.NavItem", "Navigation", icon="menu"),
        item("core.FooterColumn", "Footer columns", icon="view_week"),
        item("core.Redirect", "Redirects", icon="alt_route"),
        item("auth.User", "Staff users", icon="person"),
        item("auth.Group", "Roles", icon="admin_panel_settings"),
    ]),
]

UNFOLD = build_unfold(
    title="3 Pillars Admin",
    header="3 Pillars",
    subheader="Content & business development",
    # CI blue carries white text at 6.5:1, so it can drive Unfold's primary ramp.
    brand="#0B5EAC",
    neutral="#F5F5F7",
    navigation=ADMIN_NAVIGATION,
    dashboard_callback="apps.content.dashboard.dashboard_callback",
    site_url=SITE_URL,
    site_symbol="view_column",
    # admin-brand.css: adminkit variables. admin-apple.css: the Unfold chrome
    # (type, surfaces, controls) restyled to Apple's Human Interface Guidelines.
    extra_styles=["css/admin-brand.css", "css/admin-apple.css"],
    border_radius="10px",
    login_image="brand/login.svg",
    SITE_ICON=lambda request: static("brand/logo-mark.svg"),
    SITE_LOGO=lambda request: static("brand/logo-mark.svg"),
    SITE_FAVICONS=[{
        "rel": "icon",
        "sizes": "any",
        "type": "image/svg+xml",
        "href": lambda request: static("brand/logo-mark.svg"),
    }],
)

# Apple's system greys, light (50–400) through dark (700–950), replacing the
# generated navy-tinted ramp so surfaces and hairlines read like macOS/iOS.
UNFOLD["COLORS"]["base"] = {
    "50": "#F5F5F7",   # window background
    "100": "#EFEFF2",
    "200": "#E5E5EA",  # systemGray5 — hairlines
    "300": "#D1D1D6",  # systemGray4
    "400": "#AEAEB2",  # systemGray2
    "500": "#8E8E93",  # systemGray
    "600": "#636366",
    "700": "#48484A",
    "800": "#3A3A3C",  # dark separators
    "900": "#1C1C1E",  # dark window background
    "950": "#111112",
}
# Label colours. Secondary text is darker than systemGray so it keeps 4.5:1 on
# white (systemGray is 3.3:1).
UNFOLD["COLORS"]["font"] = {
    "subtle-light": "#6E6E73",
    "subtle-dark": "#98989D",
    "default-light": "#3A3A3C",
    "default-dark": "#E5E5EA",
    "important-light": "#1D1D1F",
    "important-dark": "#F5F5F7",
}

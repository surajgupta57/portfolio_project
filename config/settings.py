"""
Django settings for the portfolio project.
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-secret-key-change-this-before-deploying-anywhere-public"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    # Jazzmin gives the Django admin a modern, beautiful UI.
    # If it isn't installed yet, comment this line out (or run
    # `pip install django-jazzmin` — it's already in requirements.txt).
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "portfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "portfolio" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Makes SiteSettings + NavLinks available on every page,
                # including the admin login/branding if needed.
                "portfolio.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "portfolio" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Jazzmin (admin UI) configuration
# ---------------------------------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "Portfolio Admin",
    "site_header": "Portfolio CMS",
    "site_brand": "Portfolio CMS",
    "welcome_sign": "Manage every section of your website from here",
    "copyright": "Your Portfolio",
    "search_model": ["portfolio.Project", "portfolio.Experience"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "portfolio.SiteSettings",
        "portfolio.NavLink",
        "portfolio.HeroProfile",
        "portfolio.HeroStat",
        "portfolio.LedgerModule",
        "portfolio.AboutSection",
        "portfolio.AboutChip",
        "portfolio.Experience",
        "portfolio.SkillCategory",
        "portfolio.Project",
        "portfolio.EducationItem",
        "portfolio.Testimonial",
        "portfolio.ContactSection",
        "portfolio.ContactInfo",
    ],
    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "portfolio.SiteSettings": "fas fa-palette",
        "portfolio.NavLink": "fas fa-bars",
        "portfolio.HeroProfile": "fas fa-id-badge",
        "portfolio.HeroStat": "fas fa-chart-bar",
        "portfolio.LedgerModule": "fas fa-book",
        "portfolio.AboutSection": "fas fa-user-circle",
        "portfolio.AboutChip": "fas fa-tags",
        "portfolio.Experience": "fas fa-briefcase",
        "portfolio.SkillCategory": "fas fa-layer-group",
        "portfolio.Project": "fas fa-diagram-project",
        "portfolio.EducationItem": "fas fa-graduation-cap",
        "portfolio.Testimonial": "fas fa-quote-left",
        "portfolio.ContactSection": "fas fa-envelope-open-text",
        "portfolio.ContactInfo": "fas fa-address-card",
    },
    "related_modal_active": True,
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": None,
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

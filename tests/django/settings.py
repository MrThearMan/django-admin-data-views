from pathlib import Path

from django.core.management.utils import get_random_secret_key


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = get_random_secret_key()
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    #
    "django.contrib.admin",
    "admin_data_views",
    #
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #
    "tests.myapp",
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "django" / "testdb",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "cache_table",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "nice",
        },
    },
    "formatters": {
        "nice": {
            "format": "[{asctime}] {module}.{funcName}: <{levelname}> {message}",
            "datefmt": "%d/%b/%Y %H:%M:%S",
            "style": "{",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

ROOT_URLCONF = "tests.django.urls"
WSGI_APPLICATION = "tests.django.wsgi.application"
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English"), ("fi", "Finland")]
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = "/static/"

ADMIN_DATA_VIEWS = {
    # "NAME": "myapp",
    "URLS": [
        {
            "route": "foo/",
            "view": "tests.django.urls.foo_list_view",
            "name": "foo_list",
            "items": {
                "route": "<int:idd>/",
                "view": "tests.django.urls.foo_items_view",
                "name": "foo_item",
            },
        },
        {
            "route": "bar/",
            "view": "tests.django.urls.bar_list_view",
            "name": "bar_list",
            "items": {
                "route": "bar/",
                "view": "tests.django.urls.bar_items_view",
                "name": "bar_item",
            },
        },
        {
            "route": "fizz/",
            "view": "tests.django.urls.fizz_view",
            "name": "fizz",
        },
        {
            "route": "buzz/",
            "view": "tests.django.urls.buzz_view",
            "name": "buzz",
        },
        {
            "route": "complex/",
            "view": "tests.django.urls.complex_view",
            "name": "complex",
        },
    ],
}


# Documentación de `settings.py` del proyecto Django

Este documento describe la configuración incluida en la plantilla `settings.py` del proyecto Django, generado con Django 5.2.5.

---

## 1. Importaciones y configuración inicial

```python
from django.contrib.messages import constants as messages
import environ
import os
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
````

* `environ`: Para manejar variables de entorno.
* `Path`: Facilita la gestión de rutas de archivos.
* `sentry_sdk`: Para monitoreo de errores en producción.
* `messages`: Constantes de mensajes de Django.

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

* Define el directorio base del proyecto.

```python
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
```

* Inicializa django-environ para leer variables desde un archivo `.env`.

---

## 2. Configuración de seguridad y despliegue

```python
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = ["*"]
```

* `SECRET_KEY`: Clave secreta para seguridad.
* `DEBUG`: Activación del modo depuración.
* `ALLOWED_HOSTS`: Hosts permitidos (en producción se debe restringir).

---

## 3. Aplicaciones instaladas (`INSTALLED_APPS`)

### 3.1 Internas de Django

* `django.contrib.*` → Funcionalidades base (admin, auth, sesiones, mensajes, archivos estáticos, humanize).

### 3.2 Terceros

* `django_bootstrap5`, `crispy_forms`, `django_unicorn`, `djmoney`, `martor`, `formtools`.
* Herramientas para frontend, formularios, WYSIWYG, monetización y tareas.

### 3.3 Seguridad y autenticación

* `allauth` + `allauth.socialaccount.providers.google` + MFA → Autenticación avanzada con múltiples factores.

### 3.4 Aplicaciones propias

* `base.apps.BaseConfig` → App principal del proyecto.

### 3.5 Unfold

* Conjunto de aplicaciones para administración avanzada (filtros, inlines, import/export, etc.).

---

## 4. Middleware

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "allauth.usersessions.middleware.UserSessionsMiddleware",
]
```

* Incluye seguridad, manejo de sesiones, CSRF, autenticación y administración de sesiones de AllAuth.
* WhiteNoise para servir archivos estáticos en producción.

---

## 5. Templates

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "proyecto" / "templates"],
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
```

* `DIRS`: Carpeta principal de templates.
* `APP_DIRS=True` permite buscar templates dentro de cada app.
* `context_processors`: Variables globales disponibles en todas las plantillas.

---

## 6. WSGI y ASGI

```python
WSGI_APPLICATION = "proyecto.wsgi.application"
ASGI_APPLICATION = "proyecto.asgi.application"
```

* Configura los puntos de entrada para servidores WSGI y ASGI.
* Compatible con Daphne para aplicaciones asíncronas.

---

## 7. Base de datos

```python
DATABASES = {"default": env.db()}
```

* Configuración de la base de datos desde `.env`.
* Compatible con múltiples motores: PostgreSQL, MySQL, SQLite, etc.

---

## 8. Validación de contraseñas

* Validators estándar de Django:

  * `UserAttributeSimilarityValidator`
  * `MinimumLengthValidator`
  * `CommonPasswordValidator`
  * `NumericPasswordValidator`

---

## 9. Internacionalización

```python
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True
```

* Idioma español de México y zona horaria local.
* Habilita traducción y manejo de zonas horarias.

---

## 10. Archivos estáticos y media

```python
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
```

* `STATICFILES_STORAGE` con WhiteNoise optimiza archivos estáticos en producción.
* `MEDIA_ROOT` y `MEDIA_URL` para archivos subidos por usuarios.

---

## 11. Modelo de usuario

```python
AUTH_USER_MODEL = "base.User"
```

* Se usa un modelo de usuario personalizado en la app `base`.

---

## 12. AllAuth

* Login/logout:

  ```python
  LOGIN_REDIRECT_URL = "/"
  LOGOUT_REDIRECT_URL = "/"
  ACCOUNT_LOGOUT_ON_GET = True
  ```
* Métodos de autenticación: username y email.
* MFA configurado con formularios específicos.
* Formularios personalizados para login, signup y recuperación de contraseña.

---

## 13. Crispy Forms y Martor

* `CRISPY_TEMPLATE_PACK = "bootstrap5"` → Integración con Bootstrap 5.
* Martor configurado con toolbar, subida de imágenes, emoji y Markdown.

---

## 14. Celery

```python
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Mexico_City"
```

* Configuración de tareas asíncronas con Redis como broker y backend.

---

## 15. Mensajes de Django

```python
MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}
```

* Mapeo de niveles de mensajes a clases CSS de Bootstrap.

---

## 16. Caché

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://redis:6379/1"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}
```

* Configura Redis para cache de Django.

---

## 17. Logging

* Logs en `logs/django.log` y consola.
* Rotación de archivos a 5 MB, con 10 backups.
* Formato verbose: `[LEVEL] TIMESTAMP NAME MESSAGE`.

---

## 18. Sentry

```python
sentry_sdk.init(
    dsn=env("SENTRY_DSN", default=""),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace",
)
```

* Monitoreo de errores y trazas de rendimiento.
* Envía información de usuarios para diagnóstico.

---

## 19. Notas adicionales

* Se incluye soporte para **Daphne** (ASGI) con comando sugerido:

  ```bash
  daphne -b 0.0.0.0 -p 8000 proyecto.asgi:application
  ```
* Plantilla lista para desarrollo y despliegue con seguridad, cache, Celery, Sentry y autenticación avanzada.



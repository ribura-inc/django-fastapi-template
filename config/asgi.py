"""WSGI config for django-fastapi-template project."""

import os

from django.core.wsgi import get_wsgi_application

############################################
# Settings
############################################
env_state = os.getenv("ENV_STATE", "production")
if env_state == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")


############################################
# Django Application
############################################

# WSGI application
_django_app = get_wsgi_application()


def django_app(environ, start_response):  # type: ignore # noqa
    # https://ruddra.com/deploy-django-subpath-openshift/
    script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
    if script_name:
        environ["SCRIPT_NAME"] = script_name
        path_info = environ["PATH_INFO"]
        if path_info.startswith(script_name):
            environ["PATH_INFO"] = path_info[len(script_name) :]

    scheme = environ.get("HTTP_X_SCHEME", "")
    if scheme:
        environ["wsgi.url_scheme"] = scheme

    return _django_app(environ, start_response)


# urls.pyに記述されている内容をここに移植（WSGIより後に記述すること）
from django.conf import settings  # noqa
from django.contrib import admin  # noqa
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns  # noqa
from django.urls import include, path  # noqa

urlpatterns = [
    path(os.getenv("DJANGO_ADMIN_PATH", "admin/"), admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


############################################
# FastAPI Application
############################################
from django.conf import settings  # noqa
from fastapi import FastAPI, Request  # noqa
from fastapi.middleware.cors import CORSMiddleware  # noqa
from fastapi.middleware.wsgi import WSGIMiddleware  # noqa
from fastapi.responses import JSONResponse  # noqa
from fastapi.staticfiles import StaticFiles  # noqa
from app.api import api_router  # noqa
from config.fastapi_response import custom_openapi  # noqa
from fastapi_pagination import add_pagination  # noqa

fastapi_app = FastAPI(
    title="Django x FastAPI template",
    description="This is a REST API for Django x FastAPI template",
    version="0.1.0",
)
add_pagination(fastapi_app)
fastapi_app.openapi = custom_openapi(fastapi_app)  # type: ignore


@fastapi_app.exception_handler(Exception)
async def exception_handler(request: Request, e: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )


# ミドルウェアは後に追加したものが先に実行される
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routers
fastapi_app.include_router(api_router, prefix=settings.API_V1_PREFIX)


fastapi_app.mount(settings.FORCE_SCRIPT_NAME, WSGIMiddleware(django_app))


if settings.DEBUG:
    fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")
    fastapi_app.mount("/media", StaticFiles(directory="media"), name="media")

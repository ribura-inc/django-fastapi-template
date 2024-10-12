import json

from config.asgi import fastapi_app


def print_openapi() -> None:
    openapi_schema = fastapi_app.openapi()
    print(json.dumps(openapi_schema, indent=2, ensure_ascii=False))  # noqa


if __name__ == "__main__":
    print_openapi()

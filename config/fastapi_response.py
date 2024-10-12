"""OpenAPI定義にエラークラス（exceptions.py）の情報を載せる（フロントがエラーの型定義をするため）.

https://github.com/Kludex/fastapi-responses を参考に、本リポジトリ用にカスタマイズしたもの。
"""

# https://github.com/Kludex/fastapi-responses/blob/master/fastapi_responses/utils.py
import importlib
import inspect
import re
import tokenize
from collections.abc import Callable, Generator
from inspect import iscoroutinefunction, isfunction
from io import BytesIO
from tokenize import TokenInfo
from typing import Any

from fastapi.routing import BaseRoute
from starlette.exceptions import HTTPException

from config.exceptions import *  # noqa: F403


def build_statement(exc: TokenInfo, tokens: Generator[TokenInfo, None, None]) -> str:
    statement = exc.string
    while True:
        token = next(tokens)
        statement += token.string.replace("\n", "")
        if token.type == tokenize.NEWLINE:
            return statement


def is_function_or_coroutine(obj: Any) -> bool:
    return isfunction(obj) or iscoroutinefunction(obj)


def exceptions_functions(
    endpoint: Callable,
    tokens: Generator[TokenInfo, None, None],
) -> tuple[list[Exception], list[Callable]]:
    exceptions, functions = [], []
    module = importlib.import_module(endpoint.__module__)
    try:
        while True:
            token = next(tokens)
            try:
                obj = getattr(module, token.string)
                if inspect.isclass(obj):
                    statement = build_statement(token, tokens)

                    # NotFoundException(detail=f"ChatRoom(uid={uid}) not found") のようなstatementであると
                    # uidが未定義でエラーになる
                    if "Exception" in statement:
                        statement = statement.replace('f"', '"')
                        # {uid} のような部分をXXXXXに置換する
                        statement = re.sub(r"{.*?}", "XXXXX", statement)

                    http_exc = eval(statement)  # noqa
                    if isinstance(http_exc, HTTPException):
                        exceptions.append(http_exc)
                if is_function_or_coroutine(obj) and obj is not endpoint:
                    functions.append(obj)
            except Exception:  # noqa
                ...
    except StopIteration:
        ...
    return exceptions, functions  # type: ignore


def extract_exceptions(route: BaseRoute) -> list[HTTPException]:
    exceptions = []
    functions = []
    functions.append(getattr(route, "endpoint"))  # noqa: B009
    while len(functions) > 0:
        endpoint = functions.pop()
        source = inspect.getsource(endpoint)
        tokens = tokenize.tokenize(BytesIO(source.encode("utf-8")).readline)
        _exceptions, _functions = exceptions_functions(endpoint, tokens)
        exceptions.extend(_exceptions)
        functions.extend(_functions)
    return exceptions  # type: ignore


def write_response(api_schema: dict, route: BaseRoute, exc: HTTPException) -> None:
    path = getattr(route, "path")  # noqa: B009
    methods = [method.lower() for method in getattr(route, "methods")]  # noqa: B009
    for method in methods:
        status_code = str(exc.status_code)
        try:
            examples = api_schema["paths"][path][method]["responses"][status_code]["content"]["application/json"][
                "examples"
            ]
        except KeyError:
            examples = {}
        examples[exc.detail] = {"value": {"detail": exc.detail}}

        if api_schema["paths"][path][method]["responses"].get(status_code) is None:
            api_schema["paths"][path][method]["responses"][status_code] = {
                "content": {
                    "application/json": {
                        "examples": examples,
                    },
                },
            }
        else:
            api_schema["paths"][path][method]["responses"][status_code]["content"]["application/json"][
                "examples"
            ] = examples


# https://github.com/Kludex/fastapi-responses/blob/master/fastapi_responses/openapi.py
from collections.abc import Callable  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.openapi.utils import get_openapi  # noqa: E402


def custom_openapi(app: FastAPI) -> Callable:
    def _custom_openapi() -> dict:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        for route in app.routes:
            if getattr(route, "include_in_schema", None):
                for exception in extract_exceptions(route):
                    write_response(openapi_schema, route, exception)
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return _custom_openapi

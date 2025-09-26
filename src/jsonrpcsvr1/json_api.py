#
# (c) 2025 Yoichi Tanibayashi
#
import importlib
import os
from contextlib import asynccontextmanager

import click
import fastapi_jsonrpc

from pyclickutils import get_logger
from . import ENV_DEBUG, get_debug_env


def _discover_rpc_methods(prefix="rpc_"):
    """Dynamically discovers and returns RPC methods from the funcs directory.
    Only methods whose names start with the given prefix are registered.
    """
    __log = get_logger(__name__, get_debug_env(ENV_DEBUG))

    methods = []
    funcs_dir = os.path.join(os.path.dirname(__file__), "funcs")
    __log.debug("funcs_dir=%s", funcs_dir)

    for filename in os.listdir(funcs_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Remove .py extension
            module_path = f"jsonrpcsvr1.funcs.{module_name}"
            module = importlib.import_module(module_path)
            for name in dir(module):
                obj = getattr(module, name)
                if not callable(obj):
                    continue
                if not name.startswith(prefix):
                    continue
                if name.startswith("_"):
                    continue

                __log.debug("find %a", name)
                methods.append(obj)
    return methods


@asynccontextmanager
async def lifespan(api):
    """lifespan"""
    __log = get_logger(__name__, get_debug_env(ENV_DEBUG))
    __log.debug(
        "api=%s.%s", api.__module__, api.__class__.__name__
    )

    class_name = f"{api.__module__}.{api.__class__.__name__}"

    click.echo(click.style(f"[{class_name}] Start up", fg="blue"))

    yield

    click.echo(click.style(f"[{class_name}] Shutdown", fg="magenta"))


METHOD_LIST = _discover_rpc_methods(prefix="rpc_")
ENTRY_POINT_PATH = "/api"

__log = get_logger(__name__, get_debug_env(ENV_DEBUG))
__log.debug("ENV_DEBUG=%a", ENV_DEBUG)


api = fastapi_jsonrpc.API(lifespan=lifespan)
ep = fastapi_jsonrpc.Entrypoint(ENTRY_POINT_PATH)

for method in METHOD_LIST:
    __log.debug("method=%a", method.__name__)
    ep.add_method_route(method)

api.bind_entrypoint(ep)

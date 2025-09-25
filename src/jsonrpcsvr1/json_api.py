#
# (c) 2025 Yoichi Tanibayashi
#
from contextlib import asynccontextmanager
import os
import importlib
import inspect

import click
import fastapi_jsonrpc as fj



from . import ENV_DEBUG, get_logger_from_env

def _discover_rpc_methods(prefix="rpc_"):
    """Dynamically discovers and returns RPC methods from the funcs directory.
    Only methods whose names start with the given prefix are registered.
    """
    methods = []
    funcs_dir = os.path.join(os.path.dirname(__file__), "funcs")
    for filename in os.listdir(funcs_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Remove .py extension
            module_path = f"jsonrpcsvr1.funcs.{module_name}"
            module = importlib.import_module(module_path)
            for name in dir(module):
                obj = getattr(module, name)
                if callable(obj) and not name.startswith("__") and not name.startswith("_") and inspect.iscoroutinefunction(obj) and name.startswith(prefix):
                    methods.append(obj)
    return methods

METHOD_LIST = _discover_rpc_methods(prefix="rpc_")

ENTRY_POINT_PATH = "/api"

__log = get_logger_from_env(ENV_DEBUG, __name__)
__log.info("ENV_DEBUG=%a", ENV_DEBUG)


@asynccontextmanager
async def lifespan(api):
    """lifespan"""

    class_name = f"{api.__module__}.{api.__class__.__name__}"

    click.echo(click.style(f"[{class_name}] Start up", fg="blue"))

    yield

    click.echo(click.style(f"[{class_name}] Shutdown", fg="magenta"))


api = fj.API(lifespan=lifespan)
ep = fj.Entrypoint(ENTRY_POINT_PATH)

for method in METHOD_LIST:
    __log.debug("method=%a", method.__name__)
    ep.add_method_route(method)

api.bind_entrypoint(ep)

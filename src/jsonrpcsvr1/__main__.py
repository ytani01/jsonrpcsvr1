#
# (c) 2025 Yoichi Tanibayashi
#
from contextlib import asynccontextmanager

import click
import fastapi_jsonrpc as fj
import uvicorn
from pyclickutils import click_common_opts, get_logger

from jsonrpcsvr1.funcs.calc import sub, sum_int, add_each
from jsonrpcsvr1.funcs.echo import echo

from . import __version__, ENV_DEBUG, get_logger_from_env, set_debug_env

METHOD_LIST = [sum_int, sub, add_each, echo]

ENTRY_POINT_PATH = "/api"
DEF_HOST, DEF_PORT = "0.0.0.0", 8000

__log = get_logger_from_env(ENV_DEBUG, __name__)
__log.info("ENV_DEBUG=%a", ENV_DEBUG)


@asynccontextmanager
async def lifespan(app):
    """lifespan"""

    class_name = f"{app.__module__}.{app.__class__.__name__}"

    click.echo(click.style(f"[{class_name}] Start up", fg="blue"))

    yield

    click.echo(click.style(f"[{class_name}] Shutdown", fg="magenta"))


api = fj.API(lifespan=lifespan)
ep = fj.Entrypoint(ENTRY_POINT_PATH)

for method in METHOD_LIST:
    __log.debug("method=%a", method.__name__)
    ep.add_method_route(method)

api.bind_entrypoint(ep)


@click.command()
@click.option("--host", default=DEF_HOST, show_default=True)
@click.option("--port", "-p", default=DEF_PORT, show_default=True)
@click.option("--reload/--no-reload", default=True, show_default=True)
@click_common_opts(click, __version__)
def main(ctx, host, port, reload, debug):
    """JSON-RPC Server main"""

    __log = get_logger(__name__, debug)
    __log.debug("command name=%a", ctx.command.name)
    __log.debug("host=%a, port=%s, reload=%s", host, port, reload)

    set_debug_env(ENV_DEBUG, debug_flag=debug)

    uvicorn.run(f"{__name__}:api", host=host, port=port, reload=True)

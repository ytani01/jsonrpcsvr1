#
# (c) 2025 Yoichi Tanibayashi
#
import click
import uvicorn
from pyclickutils import click_common_opts, get_logger

from . import __version__, ENV_DEBUG, get_debug_env, set_debug_env


DEF_HOST, DEF_PORT = "0.0.0.0", 8000

__log = get_logger(__name__, get_debug_env(ENV_DEBUG))
__log.debug("ENV_DEBUG=%a", ENV_DEBUG)


@click.command()
@click.option("--server-host", "-s",  default=DEF_HOST, show_default=True)
@click.option("--port", "-p", default=DEF_PORT, show_default=True)
@click.option("--reload/--no-reload", default=True, show_default=True)
@click_common_opts(click, __version__)
def main(ctx, server_host, port, reload, debug):
    """JSON-RPC Server main"""

    __log = get_logger(__name__, debug)
    __log.debug("command name=%a", ctx.command.name)
    __log.debug(
        "server_host=%a, port=%s, reload=%s", server_host, port, reload
    )

    set_debug_env(ENV_DEBUG, debug_flag=debug)

    uvicorn.run(
        "jsonrpcsvr1.json_api:api", host=server_host, port=port, reload=True
    )

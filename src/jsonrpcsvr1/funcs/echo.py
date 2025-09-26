#
# (c) 2025 Yoichi Tanibayashi
#
from pyclickutils import get_logger
from .. import ENV_DEBUG, get_debug_env


async def rpc_echo(s: list[int] | str) -> list[int] | str:
    """echo"""
    __log = get_logger(__name__, get_debug_env(ENV_DEBUG))
    __log.debug("s=%s", s)
    
    return s

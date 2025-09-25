from .. import ENV_DEBUG, get_logger_from_env


# @ep.method
async def sum_int(i: list[int]) -> int:
    __log = get_logger_from_env(ENV_DEBUG, __name__)
    __log.debug("i=%s", i)

    return sum(i)


# @ep.method
async def sub(a: int, b: int) -> int:
    """sub"""
    __log = get_logger_from_env(ENV_DEBUG, __name__)
    __log.debug("a=%s, b=%s", a, b)

    return a-b

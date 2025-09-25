from .. import ENV_DEBUG, get_logger_from_env


# @ep.method
async def rpc_sum_int(i: list[int]) -> int:
    __log = get_logger_from_env(ENV_DEBUG, __name__)
    __log.debug("i=%s", i)

    return sum(i)


# @ep.method
async def rpc_sub(a: int, b: int) -> int:
    """sub"""
    __log = get_logger_from_env(ENV_DEBUG, __name__)
    __log.debug("a=%s, b=%s", a, b)

    return a-b


async def rpc_add_each(a: list[int], b: list[int]) -> list[int] | str:
    """Add each number"""
    __log = get_logger_from_env(ENV_DEBUG, __name__)
    __log.debug("a=%s, b=%s", a, b)

    try:
        c = []
        for i in range(len(a)):
            c.append(a[i] + b[i])
    except Exception as _e:
        msg = f"{type(_e).__name__}: {_e}"
        msg += f"\n    a={a}, b={b}"
        __log.error(msg)
        return msg

    __log.debug("c=%s", c)
    return c

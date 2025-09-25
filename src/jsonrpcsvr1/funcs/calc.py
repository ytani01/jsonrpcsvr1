# @ep.method
async def sum_int(i: list[int]) -> int:
    return sum(i)


# @ep.method
async def sub(a: int, b: int) -> int:
    """sub"""
    return a-b

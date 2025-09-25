#
# (c) 2025 Yoichi Tanibayashi
#
from contextlib import asynccontextmanager
import fastapi_jsonrpc as fj
import uvicorn

from . import __version__
from jsonrpcsvr1.funcs.calc import sum_int, sub
from jsonrpcsvr1.funcs.echo import echo


METHOD_LIST = [sum_int, sub, echo]

ENTRY_POINT_PATH = "/api"
DEF_HOST, DEF_PORT = "0.0.0.0", 8000


print(__file__)
print(__name__)
print(__package__)
print(__version__)

def foo(a, b):
    print(a, b)


@asynccontextmanager
async def lifespan(app: fj.API):
    """lifespan"""
    print("Start up")

    yield

    print("Shutdown")


api = fj.API(lifespan=lifespan)  # must be global for uvicorn.run()
ep = fj.Entrypoint(ENTRY_POINT_PATH)

for _f in METHOD_LIST:
    ep.add_method_route(_f)

api.bind_entrypoint(ep)  # この位置にないと、Swagger UIが機能しない(?)


def main():
    """main"""
    uvicorn.run(f"{__name__}:api", host=DEF_HOST, port=DEF_PORT, reload=True)

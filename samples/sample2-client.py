import click
import json
import requests

from pyclickutils import click_common_opts, get_logger


VERSION = "0.0.1"


@click.command()
@click.argument("rpccall", nargs=-1)
@click.option(
    "--server", "-s", type=str, default="localhost", show_default=True,
    help="server"
)
@click.option(
    "--port", "-p", type=int, default=8000, show_default=True,
    help="port number"
)
@click.option(
    "--api", "-a", type=str, default="/api", show_default=True,
    help="API path name"
)
@click_common_opts(click, VERSION)
def main(ctx, rpccall, server, port, api, debug):
    """main"""

    __log = get_logger(__name__, debug)
    __log.debug("command name = %s", ctx.command.name)
    __log.debug("server=%a, port=%s, api=%a", server, port, api)
    __log.debug("rpccall = %s", rpccall)
    if len(rpccall) % 2 == 0:
        __log.error("Invalid rpccall: %a", rpccall)
        return

    url = f"http://{server}:{port}{api}"
    __log.debug("url=%a", url)

    #
    # parse command line
    #
    method = rpccall[0]
    params = rpccall[1:]
    __log.debug("method=%a, params=%s", method, params)

    pdata = {}
    pkey_flag = True
    pkey = None
    pvalue = None
    for _p in params:
        __log.debug("_p=%a", _p)

        if pkey_flag:
            pkey_flag = False

            pkey = _p
            __log.debug("pkey=%a", pkey)

        else:
            pkey_flag = True

            pvalue = _p
            __log.debug("pvalue=%a", pvalue)

            try:
                pvalue2 = json.loads(pvalue)
            except json.decoder.JSONDecodeError:
                pvalue2 = None
            __log.debug("pvalue2=%a", pvalue2)

            if pvalue2:
                pdata[pkey] = pvalue2
            else:
                pdata[pkey] = pvalue

            __log.debug("pdata=%s", pdata)

    #
    # call rpc
    #
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": pdata,
        "id": 1
    }
    __log.debug("payload=%s", json.dumps(payload))

    response = requests.post(url, data=json.dumps(payload))

    result = response.json()
    __log.debug("result=%s", result)

    try:
        print(f"{method}{params} > {result["result"]}")
    except KeyError:
        err = result['error']
        __log.debug("error: %s", err)

        err_message = err['message']
        print(f"Error: {err_message}")

        err_data_errs = err['data']['errors']
        __log.debug("err_data_errs=%s", err_data_errs)

        for e in err_data_errs:
            print(f"  {e}")


if __name__ == "__main__":
    main()

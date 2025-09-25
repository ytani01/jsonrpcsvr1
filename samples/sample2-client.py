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

    try:
        response = requests.post(url, data=json.dumps(payload))
        result = response.json()
        __log.debug("result=%s", result)

    except requests.exceptions.ConnectionError as _e:
        __log.error("\n%s:\n %s\n", type(_e).__name__, _e)
        for _s in str(_e).split(":"):
            for _s2 in _s.split("("):
                click.echo(click.style(
                    f"{_s2.strip()}",
                    fg="red"
                ))
        return
    except Exception as _e:
        __log.error("%s: %s", type(_e).__name__, _e)
        return

    try:
        click.echo(f">> {method}{params}")
        click.echo(f"<< {result["result"]}")
    except KeyError:
        err = {}

        try:
            err = result['error']
            __log.debug("error: %s", err)
        except KeyError:
            return
        except Exception as _e2:
            __log.error("%s: %s", type(_e2).__name__, _e2)

        try:
            err_message = err['message']
            click.echo(click.style(f"Error: {err_message}", fg="red"))
        except KeyError:
            return
        except Exception as _e2:
            __log.error("%s: %s", type(_e2).__name__, _e2)

        try:
            err_data_errs = err['data']['errors']
            __log.debug("err_data_errs=%s", err_data_errs)

            for e in err_data_errs:
                click.echo(click.style(f"  {e}", fg="red"))
        except KeyError:
            return
        except Exception as _e2:
            __log.error("%s: %s", type(_e2).__name__, _e2)


if __name__ == "__main__":
    main()

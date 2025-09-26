import json
import re

import click
import requests
from pyclickutils import click_common_opts, get_logger


VERSION = "0.1.0"


@click.command()
@click.argument("rpccall", nargs=-1)
@click.option(
    "--server", "-s", type=str, default="localhost", show_default=True,
    help="server",
)
@click.option(
    "--port", "-p", type=int, default=8000, show_default=True,
    help="port number",
)
@click.option(
    "--api", "-a", type=str, default="/api", show_default=True,
    help="API path name",
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

    params_data = {}
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
                params_data[pkey] = pvalue2
            else:
                params_data[pkey] = pvalue

            __log.debug("params_data=%s", params_data)

    #
    # call rpc
    #
    payload = _mk_jsonrpc_req(method, params_data, 1)
    __log.debug("payload=%s", _format_json(payload))

    try:
        response = requests.post(url, data=json.dumps(payload))
        result = response.json()
        __log.debug("result=%s", _format_json(result))

    except requests.exceptions.ConnectionError as _e:
        _display_error(_e, __log)
        return
    except Exception as _e:
        _display_error(_e, __log)
        return

    try:
        click.echo(f">>> {method}{params}")
        click.echo(f"<<< {result["result"]}")
    except KeyError:
        _display_error(result, __log)


def _mk_jsonrpc_req(method: str, params: dict, id: int = 1) -> dict:
    """"Make JSON-RPC request"""

    jsonrpc_req = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": id,
    }
    return jsonrpc_req


def _format_json(data):
    """Formats JSON output, attempting to keep simple lists on a single line.
    """
    formatted_str = json.dumps(data, indent=2, ensure_ascii=False)

    # from
    #      [
    #         123
    #      ]
    # to
    #      [123]
    formatted_str = re.sub(r'\[\n\s*(.*?)\n\s*\]', r"[\1]", formatted_str)

    # from
    #      [
    #          123,           # 30文字以内
    #          "a"            # 30文字以内
    #      ]
    # to
    #      [123, "a"]
    formatted_str = re.sub(
        r'\[\n\s*(\S{,30})\n\s*(\S{,30})\n\s*\]', r'[\1 \2]',
        formatted_str
    )

    return formatted_str


def _display_connection_error(
    error_data: requests.exceptions.ConnectionError
):
    """Displays ConnectionError information in a readable format."""
    click.echo(
        click.style(
            f"  Connection Error Type: {type(error_data).__name__}",
            fg="red",
            bold=True,
        )
    )

    # Extract details from the exception message
    message = str(error_data)
    details = {}

    # Attempt to parse host and port from the message
    match = re.search(r"host='([^']+)', port=(\d+)", message)
    if match:
        details["Host"] = match.group(1)
        details["Port"] = int(match.group(2))

    # Attempt to parse the underlying cause
    cause_match = re.search(r"Caused by ([^:]+): (.*)", message)
    if cause_match:
        details["Cause Type"] = cause_match.group(1)
        cause_message = cause_match.group(2)

        # Further parse the cause message to remove the object repr
        obj_match = re.search(
            r"<(.*) object at 0x[0-9a-fA-F]+>: (.*)", cause_message
        )
        if obj_match:
            details["Underlying Error Type"] = obj_match.group(1)
            details["Underlying Error Message"] = obj_match.group(2)
        else:
            details["Cause Message"] = cause_message
    else:
        details["Message"] = message  # Fallback if parsing fails

    if error_data.request:
        details["Request URL"] = error_data.request.url
        details["Request Method"] = error_data.request.method
    if error_data.response:
        details["Response Status"] = error_data.response.status_code
        details["Response Text"] = error_data.response.text

    if details:
        click.echo(click.style("  Details:", fg="red"))
        click.echo(click.style(
            json.dumps(details, indent=2, ensure_ascii=False), fg="red"
        ))


def _display_error(error_data, logger):
    """Displays error information in a readable format."""
    logger.error("Error data: %s", error_data)
    click.echo(click.style("Error:", fg="red", bold=True))

    if isinstance(error_data, requests.exceptions.ConnectionError):
        _display_connection_error(error_data)
    elif isinstance(error_data, dict) and "error" in error_data:
        rpc_error = error_data["error"]
        click.echo(click.style(
            f"  RPC Error Code: {rpc_error.get('code')}", fg="red"
        ))
        click.echo(click.style(
            f"  RPC Error Message: {rpc_error.get('message')}", fg="red"
        ))
        if "data" in rpc_error:
            click.echo(click.style("  RPC Error Data:", fg="red"))
            click.echo(click.style(
                _format_json(rpc_error["data"]), fg="red"
            ))
    elif isinstance(error_data, Exception):
        click.echo(click.style(
            f"  {type(error_data).__name__}: {error_data}", fg="red"
        ))
    else:
        click.echo(click.style(f"  Message: {error_data}", fg="red"))


if __name__ == "__main__":
    main()

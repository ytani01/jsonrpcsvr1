#
# (c) 2025 Yoichi Tanibayashi
#
import os

from pyclickutils import get_logger

ENV_DEBUG = "DEBUG_jsonrpcsvr1"


def set_debug_env(debug_flag=False):
    """Set debug fulag"""
    os.environ[ENV_DEBUG] = "1" if debug_flag else "0"


def get_logger_from_env(name: str):
    """My get_logger from environment variable"""

    debug_flag: bool = os.getenv(ENV_DEBUG, "0") == "1"
    return get_logger(name, debug_flag)

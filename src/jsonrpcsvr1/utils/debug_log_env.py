#
# (c) 2025 Yoichi Tanibayashi
#
import os

from pyclickutils import get_logger


def set_debug_env(env_debug: str, debug_flag=False):
    """Set debug fulag"""
    os.environ[env_debug] = "1" if debug_flag else "0"


def get_logger_from_env(env_debug: str, name: str):
    """My get_logger from environment variable"""

    debug_flag: bool = os.getenv(env_debug, "0") == "1"
    return get_logger(name, debug_flag)

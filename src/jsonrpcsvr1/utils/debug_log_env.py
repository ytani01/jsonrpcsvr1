#
# (c) 2025 Yoichi Tanibayashi
#
import os

from pyclickutils import get_logger


def get_debug_env(env_debug: str) -> bool:
    """get debug env"""
    return os.getenv(env_debug, "0") == "1"


def set_debug_env(env_debug: str, debug_flag=False):
    """Set debug fulag"""
    os.environ[env_debug] = "1" if debug_flag else "0"

#
# (c) 2025 Yoichi Tanibayashi
#
from importlib.metadata import version as get_version

from .utils.debug_log_env import get_logger_from_env, set_debug_env


if __package__:
    __version__ = get_version(__package__)
else:
    __version__ = "0.0.0.none"

__all__ = [
    "__version__",
    "get_logger_from_env",
    "set_debug_env",
]

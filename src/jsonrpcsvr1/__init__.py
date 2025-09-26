#
# (c) 2025 Yoichi Tanibayashi
#
from importlib.metadata import version as get_version

from .utils.debug_log_env import get_debug_env, set_debug_env


if __package__:
    __version__ = get_version(__package__)
else:
    __version__ = "_._._"

ENV_DEBUG = f"DEBUG_{__package__}"

__all__ = [
    "__version__",
    "ENV_DEBUG",
    "get_debug_env",
    "set_debug_env",
]

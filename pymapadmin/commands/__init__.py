
from __future__ import annotations

from collections.abc import Mapping
from importlib.metadata import entry_points

from .base import Command

__all__ = ['load_commands']


def load_commands(group: str = 'pymapadmin.commands') \
        -> Mapping[str, type[Command]]:  # pragma: no cover
    """Load and return a map of command name to implementation class.

    Args:
        group: The entry point group used to register commands.

    """
    ret = {}
    for entry_point in entry_points(group=group):
        cls = entry_point.load()
        ret[entry_point.name] = cls
    return ret

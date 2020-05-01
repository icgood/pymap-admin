
from __future__ import annotations

from typing import Type, Mapping

from pkg_resources import iter_entry_points, DistributionNotFound

from . import Command


def load_commands(group: str = 'pymapadmin.commands') \
        -> Mapping[str, Type[Command]]:
    """Load and return a map of command name to implementation class.

    Args:
        group: The setuptools entry point used to register commands.

    """
    ret = {}
    for entry_point in iter_entry_points(group):
        try:
            cls = entry_point.load()
        except DistributionNotFound:
            pass  # optional dependencies not installed
        else:
            ret[entry_point.name] = cls
    return ret

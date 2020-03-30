import re
import textwrap
from functools import namedtuple
from pathlib import Path

from sphinx.ext.intersphinx import fetch_inventory

Settings = namedtuple("Settings", ["output_dirs", "local_only"])

ROLE_ALIASES = {
    "ref": {"label"},
    "option": {"cmdoption"},
}
ROLE_ANY = {"any"}


def get_current_role(line, column):
    """Parse current line with cursor position to get current role."""
    # Role pattern:
    # :role:`target`
    # :role:`Text <target>`
    # :domain:role:`target`
    # :domain:one:two:`target`
    role_pattern = re.compile(r"(?=:(?P<role>[a-zA-Z0-9_-]+(:[a-zA-Z0-9_-]+)*):`)")
    match = role_pattern.search(line, 0, column)
    return match.group("role") if match else None


def get_completion_list(filepath, role, settings):
    source_dir = find_source_dir(Path(filepath))
    if not source_dir:
        return []
    invdata = fetch_local_inventory(source_dir, settings.output_dirs)

    results = []
    for type_, value in invdata.items():
        if not contains_role(role, type_):
            continue
        for name, info in value.items():
            domain, priority, uri, display_name = info
            if display_name.strip() == "-":
                display_name = name
            info = textwrap.dedent(
                f"""
                {display_name}

                {domain} -> {uri}
                """
            )
            menu = f"[{type_}]"

            # Allways use absolute paths for the doc role
            if type_ == "std:doc":
                name = "/" + name.lstrip("/")
            results.append({"word": name, "menu": menu, "info": info.strip()})
    return results


def find_source_dir(filepath):
    """Find the source directory of the Sphinx project."""
    conf_file = Path("conf.py")
    source_dir = filepath.parent
    root = Path("/")
    while source_dir != root:
        path = source_dir / conf_file
        if path.exists():
            return source_dir
        source_dir = source_dir.parent
    return None


def fetch_local_inventory(source_dir, output_dirs):
    """Fetch the inventory file from the build output of the source directory."""

    class MockConfig:
        intersphinx_timeout = None
        tls_verify = False
        user_agent = None

    class MockApp:
        srcdir = ""
        config = MockConfig()

    inventory_file = Path("objects.inv")
    invdata = {}
    for output_dir in output_dirs:
        path = source_dir / output_dir / inventory_file
        if path.exists():
            invdata = fetch_inventory(MockApp(), "", str(path))
    return invdata


def contains_role(super_role, role):
    """Check if `super_role` contains `role`."""
    role = re.sub("^std:", "", role)
    super_role = re.sub("^std:", "", super_role)
    return (
        super_role in ROLE_ANY
        or role == super_role
        or role in ROLE_ALIASES.get(super_role, [])
    )

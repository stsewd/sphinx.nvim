import pickle
import re
import textwrap
from functools import namedtuple
from pathlib import Path

from sphinx.ext.intersphinx import fetch_inventory

Settings = namedtuple(
    "Settings",
    [
        "html_output_dirs",
        "doctrees_output_dirs",
        "include_intersphinx_data",
        "always_use_scoped_targets",
        "nvim",
    ],
)

ROLE_ALIASES = {
    "ref": {"label"},
    "numref": {"label"},
    "option": {"cmdoption"},
}
ROLE_ANY = {"any"}


def get_completion_list(filepath, line, column, settings):
    role = get_current_role(line, column)
    if not role:
        return []

    source_dir = find_source_dir(Path(filepath))
    if not source_dir:
        return []

    path = get_inventory_file(source_dir, settings.html_output_dirs)
    local_invdata = {}
    if path:
        local_invdata = fetch_local_inventory(path)

    intersphinx_invdata = {}

    if settings.include_intersphinx_data:
        named_inventory, unamed_inventory = fetch_intersphinx_inventories(
            source_dir, settings.doctrees_output_dirs,
        )

        if not settings.always_use_scoped_targets:
            # Named inventories shallow each other,
            # sort them to keep consistency.
            for invname, invdata in sorted(named_inventory.items()):
                for type_, value in invdata.items():
                    for name, info in value.items():
                        intersphinx_invdata.setdefault(type_, {})
                        intersphinx_invdata[type_][name] = info

        # TODO: investigate if the unamed inventory
        # already includes the named inventory.
        if not settings.always_use_scoped_targets:
            # Unamed inventories shallow the named inventories,
            # but the named ones can still be acceced with their name.
            for type_, value in unamed_inventory.items():
                for name, info in value.items():
                    intersphinx_invdata.setdefault(type_, {})
                    intersphinx_invdata[type_][name] = info

        # Generate named inventories
        for invname, invdata in named_inventory.items():
            for type_, value in invdata.items():
                for name, info in value.items():
                    intersphinx_invdata.setdefault(type_, {})
                    intersphinx_invdata[type_][f"{invname}:{name}"] = info

    # Local inventories take precedence
    for type_, value in local_invdata.items():
        for name, info in value.items():
            intersphinx_invdata.setdefault(type_, {})
            # Always use absolute paths for the doc role
            intersphinx_invdata[type_].pop(name, None)
            if type_ == "std:doc":
                name = "/" + name.lstrip("/")
            intersphinx_invdata[type_][name] = info

    return get_results(intersphinx_invdata, role)


def get_current_role(line, column):
    """
    Parse current line with cursor position to get current role.

    Valid roles:

    - :role:`target`
    - :role:`Text <target>`
    - :domain:role:`target`
    - :domain:one:two:`target`
    """

    # Find where the role name ends
    j = column
    while j >= 1:
        if line[j - 1 : j + 1] == ":`":
            break
        j -= 1

    if j <= 0:
        return None

    # Find where the role starts
    i = j
    while i >= 0:
        if line[i].isspace():
            break
        i -= 1

    i += 1
    if line[i] != ":" or i >= j:
        return None

    return line[i + 1 : j - 1]


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


def get_inventory_file(source_dir, html_output_dirs):
    inventory_file = Path("objects.inv")
    for output_dir in html_output_dirs:
        path = source_dir / output_dir / inventory_file
        if path.exists():
            return path

    return None


def fetch_local_inventory(inventory_file):
    """Fetch the inventory file from the build output of the source directory."""

    class MockConfig:
        intersphinx_timeout = None
        tls_verify = False
        user_agent = None

    class MockApp:
        srcdir = ""
        config = MockConfig()

    return fetch_inventory(MockApp(), "", str(inventory_file))


def fetch_intersphinx_inventories(source_dir, doctrees_output_dirs):
    try:
        pickle_file = Path("environment.pickle")
        for output_dir in doctrees_output_dirs:
            path = source_dir / output_dir / pickle_file
            if path.exists():
                with path.open("rb") as f:
                    env = pickle.load(f)
                named_inventory = getattr(env, "intersphinx_named_inventory", {})
                unamed_inventory = getattr(env, "intersphinx_inventory", {})
                return named_inventory, unamed_inventory
    except Exception:
        # TODO: maybe log a message
        pass
    return {}, {}


def get_results(invdata, role):
    results = []
    for type_, value in invdata.items():
        if not contains_role(role, type_):
            continue
        for name, info in value.items():
            # TODO: use a named tuple for info
            domain, priority, uri, display_name = info
            if not display_name or display_name.strip() == "-":
                display_name = name
            info = textwrap.dedent(
                f"""
                {display_name}

                {domain} -> {uri}
                """
            )
            menu = f"[{type_}]"
            results.append({"word": name, "menu": menu, "info": info.strip()})
    return results


def contains_role(super_role, role):
    """Check if `super_role` contains `role`."""
    role = re.sub("^std:", "", role)
    super_role = re.sub("^std:", "", super_role)
    return (
        super_role in ROLE_ANY
        or role == super_role
        or role in ROLE_ALIASES.get(super_role, [])
    )

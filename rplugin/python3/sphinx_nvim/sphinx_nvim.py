import pickle
import re
import textwrap
from collections import namedtuple
from pathlib import Path
from typing import List

from sphinx.ext.intersphinx import fetch_inventory

InventoryInfo = namedtuple(
    "InventoryInfo", ["domain", "priority", "uri", "display_name"]
)

Settings = namedtuple(
    "Settings",
    [
        "html_output_dirs",
        "doctrees_output_dirs",
        "include_intersphinx_data",
        "always_use_scoped_targets",
        "default_role",
        # For debug only.
        "nvim",
    ],
)

ROLE_ALIASES = {
    "ref": {"label"},
    "numref": {"label"},
    "option": {"cmdoption"},
}
ROLE_ANY = {"any"}


def get_completion_list(filepath: Path, line: str, column: int, settings: Settings):
    role = get_current_role(line, column, default=settings.default_role)
    if not role:
        return []

    source_dir = find_source_dir_from_file(Path(filepath))
    if not source_dir:
        return []

    inventory_data = get_inventory_data(source_dir, settings)
    return get_completion_results(inventory_data, role)


def get_references_list(cwd: Path, role: str, settings: Settings):
    source_dir = find_source_dir_from_cwd(cwd=cwd)
    if not source_dir:
        return []

    inventory_data = get_inventory_data(source_dir, settings)

    results = []
    for type_, value in inventory_data.items():
        if role and not contains_role(role, type_):
            continue
        for name, info in value.items():
            display_name = info.display_name
            if not display_name or display_name.strip() == "-":
                display_name = name

            label = format(f"[{type_}]", color="yellow")
            display_name = format(display_name, color="yellow", format="bold")
            name = format(name, color="blue")
            domain = format(info.domain, color="bright-white")
            arrow = format("->", color="bright-white", format="bold")
            uri = format(info.uri, color="bright-white", format="italic")
            results.append(f"{label} {display_name}  {name}  {domain} {arrow} {uri}")
    return results


def get_inventory_data(source_dir: Path, settings: Settings):
    path = find_inventory_file(source_dir, settings.html_output_dirs)
    local_invdata = {}
    if path:
        local_invdata = fetch_local_inventory(path)

    intersphinx_invdata = {}

    if settings.include_intersphinx_data:
        enviroment_file = find_enviroment_file(
            source_dir,
            settings.doctrees_output_dirs,
        )
        named_inventory, unamed_inventory = fetch_intersphinx_inventories(
            enviroment_file
        )

        if not settings.always_use_scoped_targets:
            # Named inventories shallow each other,
            # sort them to keep consistency.
            for invname, invdata in sorted(named_inventory.items()):
                for type_, value in invdata.items():
                    for name, info in value.items():
                        intersphinx_invdata.setdefault(type_, {})
                        intersphinx_invdata[type_][name] = InventoryInfo(*info)

        # TODO: investigate if the unamed inventory
        # already includes the named inventory.
        if not settings.always_use_scoped_targets:
            # Unamed inventories shallow the named inventories,
            # but the named ones can still be acceced with their name.
            for type_, value in unamed_inventory.items():
                for name, info in value.items():
                    intersphinx_invdata.setdefault(type_, {})
                    intersphinx_invdata[type_][name] = InventoryInfo(*info)

        # Generate named inventories
        for invname, invdata in named_inventory.items():
            for type_, value in invdata.items():
                for name, info in value.items():
                    intersphinx_invdata.setdefault(type_, {})
                    intersphinx_invdata[type_][f"{invname}:{name}"] = InventoryInfo(
                        *info
                    )

    # Local inventories take precedence
    for type_, value in local_invdata.items():
        for name, info in value.items():
            intersphinx_invdata.setdefault(type_, {})
            # Always use absolute paths for the doc role
            intersphinx_invdata[type_].pop(name, None)
            if type_ == "std:doc":
                name = "/" + name.lstrip("/")
            intersphinx_invdata[type_][name] = InventoryInfo(*info)

    return intersphinx_invdata


def get_current_role(line: str, column: int, default: str = "any"):
    """
    Parse current line with cursor position to get current role.

    Valid roles:

    - :role:`target`
    - :role:`Text <target>`
    - :domain:role:`target`
    - :domain:one:two:`target`

    Default role:

    - `Foo`
    - `Foo <bar>`
    """

    if column >= len(line):
        return None

    # Find where the role name ends
    for j in range(column, -1, -1):
        if line[j] == "`":
            if j == 0 or line[j - 1].isspace():
                return default
            if line[j - 1] == ":":
                break
    else:
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


def find_source_dir_from_file(filepath: Path):
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


def find_source_dir_from_cwd(cwd: Path, depth: int = 5):
    conf_file = Path("conf.py")

    if depth <= 0:
        return None

    path = cwd / conf_file
    if path.exists():
        return cwd

    for source_dir in cwd.iterdir():
        if source_dir.is_dir():
            source_dir = find_source_dir_from_cwd(source_dir, depth=depth - 1)
            if source_dir:
                return source_dir
    return None


def find_inventory_file(source_dir: Path, html_output_dirs: List[str]):
    inventory_file = Path("objects.inv")
    for output_dir in html_output_dirs:
        path = source_dir / output_dir / inventory_file
        if path.exists():
            return path

    return None


def fetch_local_inventory(inventory_file: Path):
    """Fetch the inventory file from the build output of the source directory."""

    class MockConfig:
        intersphinx_timeout = None
        tls_verify = False
        user_agent = None

    class MockApp:
        srcdir = ""
        config = MockConfig()

    return fetch_inventory(MockApp(), "", str(inventory_file))


def find_enviroment_file(source_dir: Path, doctrees_output_dirs: List[str]):
    pickle_file = Path("environment.pickle")
    for output_dir in doctrees_output_dirs:
        path = source_dir / output_dir / pickle_file
        if path.exists():
            return path
    return None


def fetch_intersphinx_inventories(enviroment_file: Path):
    if enviroment_file is None:
        return {}, {}
    try:
        with enviroment_file.open("rb") as f:
            env = pickle.load(f)
        named_inventory = getattr(env, "intersphinx_named_inventory", {})
        unamed_inventory = getattr(env, "intersphinx_inventory", {})
        return named_inventory, unamed_inventory
    except Exception:
        # TODO: maybe log a message
        pass
    return {}, {}


def get_completion_results(invdata, role: str):
    results = []
    for type_, value in invdata.items():
        if not contains_role(role, type_):
            continue
        for name, info in value.items():
            display_name = info.display_name
            if not display_name or display_name.strip() == "-":
                display_name = name
            menu_info = textwrap.dedent(
                f"""
                {display_name}

                {info.domain} -> {info.uri}
                """
            )
            menu = f"[{type_}]"
            results.append({"word": name, "menu": menu, "info": menu_info.strip()})
    return results


def contains_role(super_role: str, role: str):
    """Check if `super_role` contains `role`."""
    role = re.sub("^std:", "", role)
    super_role = re.sub("^std:", "", super_role)
    return (
        super_role in ROLE_ANY
        or role == super_role
        or role in ROLE_ALIASES.get(super_role, [])
    )


def format(text: str, color: str = None, format: str = "normal"):
    """
    Format the text using ANSI color escape sequences.

    https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
    """
    format_flags = {
        "normal": "0",
        "bold": "1",
        "italic": "3",
        "underline": "4",
    }
    color_flags = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "white": "37",
        "bright-black": "90",
        "bright-red": "91",
        "bright-green": "92",
        "bright-yellow": "93",
        "bright-blue": "94",
        "bright-white": "97",
    }
    flags = format_flags.get(format, "") + ";" + color_flags.get(color, "")
    flags = flags.strip(";")
    return f"\033[{flags}m{text}\033[0m"

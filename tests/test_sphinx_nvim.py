from pathlib import Path

import pytest
from sphinx.testing.fixtures import *  # noqa
from sphinx.testing.path import path
from sphinx_nvim.sphinx_nvim import (
    contains_role,
    fetch_intersphinx_inventories,
    fetch_local_inventory,
    find_source_dir,
    get_current_role,
)


@pytest.mark.parametrize(
    "role, line, start, end",
    [
        ("doc", "See the docs at :doc:`index`", 22, 27),
        ("ref", ":ref:`label`, foo.", 6, 11),
        ("ref", "- :ref:`label`, foo.", 8, 13),
        ("ref", "- :ref:`Text <label>`, foo.", 8, 20),
        ("py:mod", "Check the method :py:mod:`foo.bar`", 26, 33),
        ("py:mod", "Check :py:mod:`this method <foo.bar>`", 15, 36),
        ("rst:directive:option", ":rst:directive:option:`foo`", 23, 26),
        ("ref", ":doc:`foo`, :ref:`this`.", 18, 22),
        ("ref", ":doc:`foo`, :ref:`this`.", 18, 22),
        ("any", "`default` role", 1, 8),
        ("any", "default `role`.", 9, 13),
    ],
)
def test_get_current_role(role, line, start, end):
    for i in range(start, end + 1):
        assert role == get_current_role(line, i)


@pytest.mark.parametrize(
    "file, dir",
    [
        ("data/docs/index.rst", "data/docs/"),
        ("data/docs/nested/index.rst", "data/docs/"),
        ("data/docs-src/source/index.rst", "data/docs-src/source/"),
        ("data/docs-src/source/nested/index.rst", "data/docs-src/source/"),
    ],
)
def test_find_source_dir(file, dir):
    cwd = Path(__file__).parent
    file = cwd / file
    dir = cwd / dir
    assert dir == find_source_dir(file)


@pytest.mark.parametrize(
    "expected, super_role, role",
    [
        (True, "ref", "ref"),
        (True, "ref", "std:ref"),
        (True, "any", "std:ref"),
        (True, "any", "ref"),
        (True, "any", "doc"),
        (True, "any", "downloads"),
        (True, "any", "py:class"),
        (True, "ref", "label"),
        (True, "ref", "std:label"),
        (True, "std:ref", "label"),
        (True, "std:ref", "std:label"),
        (True, "py:class", "py:class"),
        (True, "std:option", "std:cmdoption"),
        (True, "option", "cmdoption"),
        (True, "numref", "std:label"),
        (False, "ref", "doc"),
        (False, "std:label", "std:doc"),
        (False, "doc", "downloads"),
        (False, "py:class", "py:method"),
    ],
)
def test_contains_role(expected, super_role, role):
    assert expected is contains_role(super_role, role)


def test_fetch_local_inventory(make_app):
    cwd = Path(__file__).parent
    srcdir = path(str(cwd / "data/docs/"))
    app = make_app("html", srcdir=srcdir)
    app.build(force_all=True)

    path_to_inv = Path(app.outdir) / "objects.inv"
    result = fetch_local_inventory(path_to_inv)

    expected = {
        "std:label": {
            "genindex": ("Test", "", "genindex.html", "Index"),
            "index:indices and tables": (
                "Test",
                "",
                "index.html#indices-and-tables",
                "Indices and tables",
            ),
            "index:welcome to test's documentation!": (
                "Test",
                "",
                "index.html#welcome-to-test-s-documentation",
                "Welcome to Test’s documentation!",
            ),
            "modindex": ("Test", "", "py-modindex.html", "Module Index"),
            "py-modindex": ("Test", "", "py-modindex.html", "Python Module Index"),
            "search": ("Test", "", "search.html", "Search Page"),
        },
        "std:doc": {
            "index": ("Test", "", "index.html", "Welcome to Test’s documentation!")
        },
    }

    assert result == expected


def test_fetch_intersphinx_inventories(make_app):
    cwd = Path(__file__).parent

    srcdir = path(str(cwd / "data/docs-src/source"))
    app = make_app("html", srcdir=srcdir)
    app.build()
    inv_file = Path(app.outdir) / "objects.inv"

    srcdir = path(str(cwd / "data/docs/"))
    app = make_app(
        "html",
        srcdir=srcdir,
        confoverrides={
            "intersphinx_mapping": {
                "python": ("https://docs.python.org/3", str(inv_file)),
            },
        },
    )
    app.build()

    path_to_environment = Path(app.doctreedir) / "environment.pickle"
    result = fetch_intersphinx_inventories(path_to_environment)
    expected = (
        {
            "python": {
                "std:label": {
                    "genindex": (
                        "Test src",
                        "",
                        "https://docs.python.org/3/genindex.html",
                        "Index",
                    ),
                    "modindex": (
                        "Test src",
                        "",
                        "https://docs.python.org/3/py-modindex.html",
                        "Module Index",
                    ),
                    "py-modindex": (
                        "Test src",
                        "",
                        "https://docs.python.org/3/py-modindex.html",
                        "Python Module Index",
                    ),
                    "search": (
                        "Test src",
                        "",
                        "https://docs.python.org/3/search.html",
                        "Search Page",
                    ),
                },
                "std:doc": {
                    "index": (
                        "Test src",
                        "",
                        "https://docs.python.org/3/index.html",
                        "Welcome to Test src’s documentation!",
                    )
                },
            }
        },
        {
            "std:label": {
                "genindex": (
                    "Test src",
                    "",
                    "https://docs.python.org/3/genindex.html",
                    "Index",
                ),
                "modindex": (
                    "Test src",
                    "",
                    "https://docs.python.org/3/py-modindex.html",
                    "Module Index",
                ),
                "py-modindex": (
                    "Test src",
                    "",
                    "https://docs.python.org/3/py-modindex.html",
                    "Python Module Index",
                ),
                "search": (
                    "Test src",
                    "",
                    "https://docs.python.org/3/search.html",
                    "Search Page",
                ),
            },
            "std:doc": {
                "index": (
                    "Test src",
                    "",
                    "https://docs.python.org/3/index.html",
                    "Welcome to Test src’s documentation!",
                )
            },
        },
    )
    assert result == expected

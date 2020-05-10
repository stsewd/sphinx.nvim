from pathlib import Path

import pytest
from sphinx_nvim.sphinx_nvim import contains_role, find_source_dir, get_current_role


@pytest.mark.parametrize(
    "role, line, start, end",
    [
        ("doc", "See the docs at :doc:`index`", 22, 27),
        ("ref", ":ref:`label`, foo.", 6, 11),
        ("ref", "- :ref:`label`, foo.", 8, 13),
        ("ref", "- :ref:`Text <label>`, foo.", 8, 19),
        ("py:mod", "Check the method :py:mod:`foo.bar`", 26, 34),
        ("py:mod", "Check :py:mod:`this method <foo.bar>`", 15, 36),
        ("rst:directive:option", ":rst:directive:option:`foo`", 23, 26),
        ("ref", ":doc:`foo`, :ref:`this`.", 18, 22),
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
        (False, "ref", "doc"),
        (False, "std:label", "std:doc"),
        (False, "doc", "downloads"),
        (False, "py:class", "py:method"),
    ],
)
def test_contains_role(expected, super_role, role):
    assert expected is contains_role(super_role, role)

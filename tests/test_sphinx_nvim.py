from pathlib import Path

import pytest
from sphinx_nvim.sphinx_nvim import contains_role, find_source_dir, get_current_role


@pytest.mark.parametrize(
    "role, line, max_index",
    [
        ("doc", "See the docs at :doc:`index`", 7),
        ("ref", ":ref:`label`, foo.", 12),
        ("ref", "- :ref:`label`, foo.", 12),
        ("ref", "- :ref:`Text <label>`, foo.", 19),
        ("py:mod", "Check the method :py:mod:`foo.bar`", 8),
        ("py:mod", "Check :py:mod:`this method <foo.bar>`", 22),
        ("rst:directive:option", ":rst:directive:option:`foo`", 4),
    ],
)
def test_get_current_role(role, line, max_index):
    for i in range(len(line) - 1, len(line) - max_index, -1):
        assert role == get_current_role(line, i)


@pytest.mark.parametrize(
    "file, dir",
    [
        ("docs/index.rst", "docs/"),
        ("docs/nested/index.rst", "docs/"),
        ("docs-src/source/index.rst", "docs-src/source/"),
        ("docs-src/source/nested/index.rst", "docs-src/source/"),
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
        (False, "ref", "doc"),
        (False, "std:label", "std:doc"),
        (False, "doc", "downloads"),
        (False, "py:class", "py:method"),
    ],
)
def test_contains_role(expected, super_role, role):
    assert expected is contains_role(super_role, role)

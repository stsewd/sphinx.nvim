import os
from pathlib import Path

import nox

files = ["rplugin/python3", "tests", "noxfile.py"]


@nox.session
def test(session):
    cwd = os.getcwd()
    session.virtualenv.env = {"PYTHONPATH": str(cwd / Path("rplugin/python3"))}
    session.install("pytest", "pynvim", "sphinx")
    session.run("pytest", *session.posargs)


@nox.session
def format(session):
    """Run black code formater."""
    session.install("black", "isort")
    session.run("isort", "--profile", "black", *files)
    session.run("black", *files)


@nox.session
def lint(session):
    session.install("flake8", "black")
    session.run("black", "--check", *files)
    session.run("flake8", *files)

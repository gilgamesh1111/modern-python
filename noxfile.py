"""nox sessions."""

import nox
from nox.sessions import Session

nox.options.default_venv_backend = "uv"
nox.options.sessions = "lint", "audit", "tests"


@nox.session(python=["3.11", "3.12"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("uv", "sync", external=True)
    session.run("pytest", *args)


@nox.session(python="3.11")
def audit(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    session.run("pip-audit", external=True)


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.11", "3.12"])
def lint(session: Session) -> None:
    """Lint using ruff."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", *args)


@nox.session(python="3.11")
def format(session: Session) -> None:
    """Format using ruff."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", *args, "--fix")


package = "modern_python"


@nox.session(python=["3.11"])
def typeguard(session):
    """Run typeguard when testing."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("uv", "sync", external=True)
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python="3.11")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("uv", "sync", external=True)
    session.install(
        "myst-parser",
        "sphinx",
        "sphinx-autodoc-typehints",
        "sphinx-autodoc2",
        "sphinx_rtd_theme",
    )
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python=["3.8", "3.7"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("uv", "sync", external=True)
    session.run("xdoctest", package, *args)

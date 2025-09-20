import nox
from nox.sessions import Session

nox.options.default_venv_backend = "uv"
nox.options.sessions = "lint", "audit", "tests"


@nox.session(python=["3.11", "3.12"])
def tests(session: Session) -> None:
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("uv", "sync", external=True)
    session.run("pytest", *args)


@nox.session(python="3.11")
def audit(session: Session) -> None:
    session.run("pip-audit", external=True)


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.11", "3.12"])
def lint(session: Session) -> None:
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", *args)


@nox.session(python="3.11")
def format(session: Session) -> None:
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", *args, "--fix")


package = "modern_python"


@nox.session(python=["3.11"])
def typeguard(session):
    args = session.posargs or ["-m", "not e2e"]
    session.run("uv", "sync", external=True)
    session.run("pytest", f"--typeguard-packages={package}", *args)


def install_with_constraints(session, *args, **kwargs):
    try:
        session.run(
            "uv",
            "export",
            "--no-hashes",
            "--format=requirements-txt",
            "-o",
            "constraints.txt",
            silent=True,
        )
        session.install("-c", "constraints.txt", *args, **kwargs)
    finally:
        # os.remove("constraints.txt")
        ...


@nox.session
def t(session: Session) -> None:
    session.run("uv", "sync", external=True)
    session.run("where", "mkdocs", external=True)
    session.run("mkdocs", "-V")


@nox.session(python="3.11")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("uv", "sync", "--dev", external=True)
    session.run("sphinx-build", "docs", "docs/_build")

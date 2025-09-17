import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = "lint", "audit", "tests"


@nox.session(python=["3.11", "3.12"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("uv", "sync", external=True)
    session.run("pytest", *args)


@nox.session(python="3.11")
def audit(session):
    session.run("pip-audit", external=True)

import nox

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.11", "3.12"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("uv", "install", external=True)
    session.run("pytest", *args)

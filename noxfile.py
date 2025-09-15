import os

import nox
from nox.sessions import Session

locations = "src", "tests", "noxfile.py", "docs/conf.py"


def install_with_constraints(session: Session, *args: str, **kwargs: dict) -> None:
    """Install packages with pip, using constraints.txt if it exists."""
    constraints_file = ".constraints.txt"
    try:
        session.run(
            "uv",
            "export",
            "--dev",
            "--no-hashes",
            "--output-file",
            constraints_file,
            external=True,
            silent=True,
        )
        session.install(
            f"--constraint={constraints_file}",
            *args,
            **kwargs,
        )
    finally:
        pass
    # finally:
    #     if os.path.exists(constraints_file):
    #         os.remove(constraints_file)


@nox.session(python="3.11")
def docs(session: Session) -> None:
    """Build the documentation."""
    install_with_constraints(
        session, "sphinx", "sphinx-autodoc-typehints", "myst-parser", "sphinx-rtd-theme"
    )
    session.run("sphinx-build", "docs", "docs/_build")

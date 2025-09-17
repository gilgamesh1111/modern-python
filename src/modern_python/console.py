import textwrap

import click

from modern_python import __version__, wikipedia


@click.option(
    "--language",
    "-l",
    default="en",
    help="Language edition of Wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.command()
@click.version_option(version=__version__)
def main(language: str) -> None:
    """The modern Python project."""
    page = wikipedia.random_page(language=language)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))


if __name__ == "__main__":
    main()

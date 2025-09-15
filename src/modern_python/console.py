import textwrap

import click

from modern_python import __version__, wikipedia


@click.command()
@click.version_option(version=__version__)
def main():
    """The modern Python project."""
    data = wikipedia.random_page()

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))


if __name__ == "__main__":
    main()

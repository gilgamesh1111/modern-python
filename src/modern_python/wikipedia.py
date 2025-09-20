import click
import pydantic
import requests
from pydantic import BaseModel

API_URL = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(HTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    )
}


class Page(BaseModel):
    """Page resource.

    Attributes:
        title: The title of the Wikipedia page.
        extract: A plain text summary.

    """

    title: str
    extract: str


def random_page(language: str = "en") -> Page:
    """Return a random page.

    Performs a GET request to the /page/random/summary endpoint.

    Args:
        language: The Wikipedia language edition. By default, the English
            Wikipedia is used ("en").

    Returns:
        A page resource.

    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.

    """
    url = API_URL.format(language=language)
    try:
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()
            return Page.model_validate(response.json())
    except (requests.RequestException, pydantic.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)


if __name__ == "__main__":
    data = random_page()

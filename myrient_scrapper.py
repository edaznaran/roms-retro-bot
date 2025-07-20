"""
This module contains the MyrientScrapper class which is used to scrape game information from
a specified URL using BeautifulSoup.
"""

from dataclasses import dataclass
from uuid import uuid4

from bs4 import BeautifulSoup, Tag
from telegram import InlineQueryResultDocument


@dataclass
class MyrientScrapper:
    """A class used to scrape game information from the Myrient website.

    :param url:
    The base URL of the Myrient website.
    :param soup:
    The BeautifulSoup object containing the parsed HTML of the Myrient webpage.
    """
    url: str
    soup: BeautifulSoup


def get_games(scrapper: MyrientScrapper,
              query) -> list[InlineQueryResultDocument]:
    """Retrieves a list of games that match the given query."""
    formatted_query = _format_query(query)
    table_cells = scrapper.soup.select("tr > td")

    # The games are stored in groups of 3 in the table_cells list.
    games: list[list[Tag]] = []
    for i in range(0, len(table_cells), 3):
        a_tag = table_cells[i].a
        if a_tag is None or a_tag.get("title") is None:
            continue
        if all(x in a_tag["title"] for x in formatted_query):
            games.append(table_cells[i:i + 3])

    count = 0
    results: list[InlineQueryResultDocument] = []
    for game in games:
        result = _make_results(game, scrapper.url)
        if result is None:
            count -= 1
            continue
        results.append(result)
        if count == 9:
            break
        count += 1
    return results


def _make_results(
    game: list[Tag], base_url: str
) -> InlineQueryResultDocument | None:
    """Creates InlineQueryResultDocument objects from game data."""
    a_tag = game[0].a
    if a_tag is None:
        return None
    game_name = a_tag.get("title")
    game_ref = a_tag.get("href")
    if game_name is None or game_ref is None:
        return None
    game_name = str(game_name)
    game_ref = str(game_ref)
    sec1 = game_name.find("(") + 1
    sec2 = game_name.find("(", sec1)
    dot_index = game_name.rfind(".")

    if sec2 == -1:
        sec2 = dot_index + 1
        languages = ""
    else:
        languages = game_name[sec2:dot_index]
    # description = game_name[sec1:dot_index]
    regions = game_name[sec1:sec2 - 2]
    size = game[1].get_text()

    print(game_name + " - " + size)

    splitted_size = size.split()
    if splitted_size[1] == "GiB" or (
        splitted_size[1] == "MiB" and float(splitted_size[0]) > 20
    ):
        return None

    return InlineQueryResultDocument(
        id=str(uuid4()),
        title=game_name[0:sec1 - 2],
        document_url=base_url + game_ref,
        mime_type="application/zip",
        description=size + " - " + regions + " " + languages,
    )


def _format_query(query: str) -> list[str]:
    """Formats the given query string for use in the Myrient website."""
    if query == "":
        return [""]
    splitted_query = []
    for index, word in enumerate(query.split()):
        if index == 0 or len(word) > 3:
            splitted_query.append(word.capitalize())
        else:
            splitted_query.append(word)
    return splitted_query

"""
This module contains the MyrientScrapper class which is used to scrape game information from
a specified URL using BeautifulSoup.
"""

from dataclasses import dataclass
from uuid import uuid4

from bs4 import BeautifulSoup
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


async def get_games(scrapper: MyrientScrapper, query):
    """Retrieves a list of games that match the given query."""
    formatted_query = _format_query(query)
    table_cells = scrapper.soup.select("tr > td")

    # The games are stored in groups of 3 in the table_cells list.
    games = []
    for i in range(0, len(table_cells), 3):
        a_tag = table_cells[i].a
        if a_tag is None or a_tag.get("title") is None:
            continue
        if all(x in a_tag["title"] for x in formatted_query):
            games.append(table_cells[i:i + 3])

    response = _make_results(games, scrapper.url)
    return response


def _make_results(games, base_url):
    """Creates InlineQueryResultDocument objects from game data."""
    count = 0
    results = []
    for game in games:
        game_name = game[0].a.get("title")
        game_ref = game[0].a.get("href")
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
            count -= 1

        else:
            results.append(
                InlineQueryResultDocument(
                    id=str(uuid4()),
                    title=game_name[0:sec1 - 2],
                    document_url=base_url + game_ref,
                    mime_type="application/zip",
                    description=size + " - " + regions + " " + languages,
                )
            )
        if count == 9:
            break
        count += 1
    return results


def _format_query(query):
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

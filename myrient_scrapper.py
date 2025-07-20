"""
This module contains the MyrientScrapper class which is used to scrape game information from
a specified URL using BeautifulSoup.
"""

from uuid import uuid4

from telegram import InlineQueryResultDocument


class MyrientScrapper:
    """
    A class used to scrape game information from the Myrient website.
    Attributes
    ----------
    url : str
        The base URL of the Myrient website.
    soup : BeautifulSoup
        The BeautifulSoup object containing the parsed HTML of the Myrient webpage.
    """
    def __init__(self, url, soup):
        self.url = url
        self.soup = soup

    async def get_games(self, query):
        """Retrieves a list of games that match the given query."""
        formatted_query = self._format_query(query)
        table_cells = self.soup.select("tr > td")

        # The games are stored in groups of 3 in the table_cells list.
        games = []
        for i in range(0, len(table_cells), 3):
            if table_cells[i].a.get("title") is None:
                continue
            if all(x in table_cells[i].a["title"] for x in formatted_query):
                games.append(table_cells[i:i + 3])

        response = self._make_results(games)
        return response

    def _make_results(self, games):
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
                        document_url=self.url + game_ref,
                        mime_type="application/zip",
                        description=size + " - " + regions + " " + languages,
                    )
                )
            if count == 9:
                break
            count += 1
        return results

    def _format_query(self, query):
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

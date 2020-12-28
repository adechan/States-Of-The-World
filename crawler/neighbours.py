import re

import requests
from bs4 import BeautifulSoup


def get_land_neighbours_from_table(td, countries):
    """
   Extract the land neighbours from the table
   :return: list of all land neighbours
   """
    div = td.find("div", class_="mw-collapsible-content")
    neighbours = set()

    # we don't have any land neighbours
    # so the div doesn't exist
    if div is None:
        neighbours = []

    if div is not None:
        # removes all the <small> tags
        small_s = div.findAll("small")
        if len(small_s) != 0:
            for small in small_s:
                div.small.decompose()


        a_s = div.findAll("a")

        all_neighbours = []
        for a in a_s:
            link = a.get("href")
            name = a.text.strip()
            all_neighbours.append((name, link))


        for neighbour in all_neighbours:
            found_neighbour = None

            for country in countries:
                link = country[1]
                name = country[0]

                if neighbour[1] == link or neighbour[0].strip() == name.strip():
                    found_neighbour = country

            if found_neighbour is None:
                continue

            neighbours.add(found_neighbour[0].strip())

    return list(neighbours)

def get_maritime_neighbours_from_table(td, countries):
    """
    Extract the maritime neighbours from the table
    :return: list of all maritime neighbours
    """
    neighbours = set()

    while td.find("i"):
        td.i.decompose()

    while td.find("sup"):
        td.sup.decompose()

    r = re.compile('\\(<a[\\w\\s="<>/_-]*>[\\w\\s="<>/_-]*</a>\\)')
    text = re.sub(r, "", td.text.strip())

    r = re.compile('\\([\\w\\s_-]*\\)')
    text = re.sub(r, "", text)

    text = text.replace('\xa0', '\n')

    countries_found = []
    if len(text) > 0:
        for country in text.split("\n"):
            if country.strip() not in countries_found:
                countries_found.append(country.strip())


    if len(td) == 0 or td is None:
        neighbours = []

    if len(td) != 0 or td is not None:
        a_s = td.findAll("a")

        all_neighbours = []
        for a in a_s:
            link = a.get("href")
            name = a.text.strip()

            if name in countries_found:
                all_neighbours.append((name, link))


        for neighbour in all_neighbours:
            found_neighbour = None

            for country in countries:
                link = country[1]
                name = country[0]

                if neighbour[1] == link or neighbour[0].strip() == name.strip():
                    found_neighbour = country

            if found_neighbour is None:
                continue

            neighbours.add(found_neighbour[0].strip())

    return list(neighbours)


def get_land_neighbours(country_name, country_link, countries):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders
    to get all the land neighbours for a given country.
    :return: list of land neighbours
    """
    root = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")
    t_body = table.find("tbody")

    tr_s = t_body.findAll("tr")

    neighbours = []
    for tr in tr_s:
        td_s = tr.findAll("td")

        if len(td_s) == 0:
            continue

        r_name = re.compile("([\\w\\s,]*)")
        name = re.search(r_name, str(td_s[0].text.strip())).group(0)
        if name == country_name:
            neighbours.extend(get_land_neighbours_from_table(td_s[5], countries))

    # if we can't find a match using the name of the country
    # then we try to find a match on the link
    if len(neighbours) == 0:
        for tr in tr_s:
            td_s = tr.findAll("td")

            if len(td_s) == 0:
                continue

            a_s = td_s[0].findAll("a")
            for a in a_s:
                link = a.get("href")
                if link == country_link:
                    neighbours.extend(get_land_neighbours_from_table(td_s[5], countries))

    return neighbours

def get_maritime_neighbours(country_name, country_link, countries):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_maritime_boundaries
    to get all the maritime neighbours for a given country.
    :return: list of maritime neighbours
    """
    root = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_maritime_boundaries"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")
    t_body = table.find("tbody")

    tr_s = t_body.findAll("tr")

    neighbours = []
    for tr in tr_s:
        td_s = tr.findAll("td")

        if len(td_s) == 0:
            continue

        r_name = re.compile("([\\w\\s,]*)")
        name = re.search(r_name, str(td_s[0].text.strip())).group(0)
        if name == country_name:
            neighbours.extend(get_maritime_neighbours_from_table(td_s[4], countries))

    # if we can't find a match using the name of the country
    # then we try to find a match on the link
    if len(neighbours) == 0:
        for tr in tr_s:
            td_s = tr.findAll("td")

            if len(td_s) == 0:
                continue

            a_s = td_s[0].findAll("a")
            for a in a_s:
                link = a.get("href")
                if link == country_link:
                    neighbours.extend(get_maritime_neighbours_from_table(td_s[4], countries))

    return neighbours


def get_neighbours(country_name, country_link, countries):
    """
    Get all land and maritime neighbours for each country
    :return: dictionary that has in the key "land" all the land neighbours
             and in the "maritime" key all the maritime neighbours
    """
    neighbours = {}
    neighbours["land"] = get_land_neighbours(country_name, country_link, countries)
    neighbours["maritime"] = get_maritime_neighbours(country_name, country_link, countries)

    return neighbours
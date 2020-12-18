import re

import requests
from bs4 import BeautifulSoup

def split_camel_case_words(word):
    """
    input: HelloHello
    output: ['Hello', 'Hello']
    :param word: string that we want to split
    :return: list of words found when we split ex. "LowerUpper" into ["Lower", "Upper"]
    """
    words = []

    for index, letter in enumerate(word):
        # if it's the end of the string, then just take the word
        if index + 1 >= len(word):
            words.append(word)
            break

        # current letter - lower && next letter - upper
        if word[index].islower() and word[index + 1].isupper():
            words.append(word[0: index + 1])
            words.extend(split_camel_case_words(word[index + 1: len(word)]))
            break

    return words

def get_land_neighbours_from_table(td_s, countries):
    """
    We look in the row where we found a match for the country name, and we get all of the land neighbours
    from the 4th column found in that row.
    :param td_s: list of all td's where we found a country name/ country link match
    :return: list of all *land* neighbours for that country
    """
    # splits by <br>
    all_neighbours = td_s[4].text.strip().split("\xa0")

    countries_found = []
    for country in all_neighbours:
        # we only add the land neighbours
        # -> the ones that have (L), (M/L) or nothing
        if "(M)" not in country:
            country_sub = re.sub("\\[[0-9]*\\]", "", country)   # get rid of notes
            country_name = country_sub.replace(" (L)", "")      # get rid of (L)
            country_name = country_name.replace(" (M/L)", "")   # get rid of (M/L)

            countries_found.extend(split_camel_case_words(country_name.strip()))

    # for each country name found earlier, we also find the link
    countries_found_links = []
    for link in td_s[4].findAll("a"):
        if link.text in countries_found:
            countries_found_links.append(link.get("href"))

    neighbours = []
    # for each link we check to see if it exists in our main list of countries
    # and if it does, then we add the name of the country that has that link in the list of neighbours
    for neighbour_link in countries_found_links:
        found_neighbour = None

        for country in countries:
            link = country[1]
            if neighbour_link == link:
                found_neighbour = country

        if found_neighbour is None:
            continue

        neighbours.append(found_neighbour[0].strip())

    return neighbours

def get_all_neighbours_from_table(td_s, countries):
    """
    We look in the row where we found a match for the country name, and we get all neighbours
    from the 4th column found in that row.
    :param td_s: list of all td's where we found a country name/ country link match
    :return: list of *all* neighbours for that country
    """
    all_neighbours = []

    # removes all the <small> tags
    small_s = td_s[4].findAll("small")
    if len(small_s) != 0:
        for small in small_s:
            td_s[4].small.decompose()

    a_s = td_s[4].findAll("a")

    # gets name of the country and the link for each country found in the column
    for a in a_s:
        all_neighbours.append((a.text, a.get("href")))

    neighbours = []
    # for each country found we check to see if the name or the link exists in our main list of countries
    # and if it does, then we add the name of the country in the list of neighbours
    for neighbour in all_neighbours:
        found_neighbour = None

        for country in countries:
            link = country[1]
            name = country[0]

            if neighbour[1] == link or neighbour[0].strip() == name.strip():
                found_neighbour = country

        if found_neighbour is None:
            continue

        neighbours.append(found_neighbour[0].strip())

    return neighbours


def get_neighbours(country_name, country_link, countries):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_and_maritime_borders
    to get all the neighbours
    :param country_name: name of the country
    :param country_link: link of the country
    :return: list with all the country's neighbours
    """
    root = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_and_maritime_borders"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")
    t_body = table.find("tbody")

    neighbours = []
    tr_s = t_body.findAll("tr")
    for tr in tr_s:
        td_s = tr.findAll("td")

        if len(td_s) == 0:
            continue

        r_name = re.compile("([\\w\\s,]*)")
        name = re.search(r_name, str(td_s[0].text.strip())).group(0)

        if name == country_name:
            neighbours.extend(get_all_neighbours_from_table(td_s, countries))

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
                    neighbours.extend(get_all_neighbours_from_table(td_s, countries))

    return neighbours
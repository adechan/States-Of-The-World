import re

import requests
from bs4 import BeautifulSoup


def get_all_government_systems():
    """
    Crawls https://en.wikipedia.org/wiki/List_of_countries_by_system_of_government to get all possible
    governments.
    :return: list with all governments
    """
    root = "https://en.wikipedia.org/wiki/List_of_countries_by_system_of_government"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")

    table_body = table.find("tbody")
    tr_s = table_body.findAll("tr")

    government_systems = []
    for tr in tr_s:
        td_s = tr.findAll("td")

        if len(td_s) == 0:
            continue

        if td_s[1].text.replace("\xa0", " ").strip() not in government_systems:
            government_systems.append(td_s[1].text.replace("\xa0", " ").strip())

    return government_systems


def is_government_tr(tr):
    """
    Checks to see if the current <tr> is a row that contains information about government.
    :param tr: current row
    :return: True, if it contains information about government, False otherwise
    """
    th = tr.find('th')
    if th is not None:
        match = re.search("\\s*Government\\s*", th.text)
        if match is not None:
            return True

    return False


def get_government_system(country_name, country_link):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_countries_by_system_of_government to get the form of
    government for each country.
    :param country_name: name of the country
    :param country_link: link of the country
    :return: the form of government in the given country
    """
    root = "https://en.wikipedia.org/wiki/List_of_countries_by_system_of_government"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")

    table_body = table.find("tbody")
    tr_s = table_body.findAll("tr")

    government_systems = get_all_government_systems()

    system_of_government = ""
    for tr in tr_s:
        td_s = tr.findAll("td")

        if len(td_s) == 0:
            continue

        if td_s[0].text.strip() == country_name:
            system_of_government = td_s[1].text.strip()

    # if we didn't find a match in the first table,
    # then we look in the country's table using the link
    governments_found = []
    if system_of_government == "":
        root = "https://en.wikipedia.org" + country_link
        page = requests.get(root)
        body = BeautifulSoup(page.content, "html.parser")
        table = body.find("table", class_="geography")

        tr_s = table.findAll("tr")

        for tr in tr_s:
            if is_government_tr(tr):
                td = tr.find("td")
                a_s = td.findAll("a")
                for a in a_s:
                    r = re.compile('>([a-zA-Z -]*)\\s*</a>')
                    match = re.search(r, str(a))
                    if match:
                        governments_found.append(match.group(1))

        # get the form of government which is in our initial list of governments
        for government in government_systems:
            for government_found in governments_found:
                if government.lower() in government_found.lower():
                    system_of_government = government.capitalize()

    return system_of_government

import re

import requests
from bs4 import BeautifulSoup


def is_area_tr(tr):
    """
    Find the row that contains information about the area.
    :param tr: a row in the table
    :return: True, if it contains information about area, False otherwise.
    """
    th = tr.find('th')
    if th is not None:
        match = re.search("•\\s+(Total|Land)", th.text)
        if match is not None:
            return True

    return False

def get_area(country_name, country_link):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area to get
    the area of the country. If we don't find the information on this page, then we use the
    country's link and search for the area in that country's table.
    :param country_name: name of the country
    :param country_link: backup link to search in if we couldn't find the area in the first table
    :return: the area of the country in km².
    """
    root = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")

    table_body = table.find("tbody")
    tr_s = table_body.findAll("tr")

    area = ""
    for tr in tr_s:
        td_s = tr.findAll("td")
        for td in td_s:

            # if we find a match using the full name of country
            # or we find a match skipping "The "
            if (country_name == td.text.strip() or country_name[4:] == td.text.strip()) and td_s[0].text != "–":
                r = re.compile("[0-9,.]*")
                if re.search(r, td_s[2].text.strip()):
                    area = re.search(r, td_s[2].text.strip()).group(0)

    # if we didn't find in the first table, then we look in the country's table
    if area == "":
        root = "https://en.wikipedia.org" + country_link
        page = requests.get(root)
        body = BeautifulSoup(page.content, "html.parser")
        table = body.find("table", class_="geography")

        tr_s = table.findAll("tr")

        area = ""
        for tr in tr_s:
            if is_area_tr(tr):
                td = tr.find("td")
                r = re.compile("[0-9][0-9,]*")
                if re.search(r, td.text):
                    area = re.search(r, td.text).group(0)

                if area != "":
                    break

    return area

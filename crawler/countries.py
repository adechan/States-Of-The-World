import io

import requests
from bs4 import BeautifulSoup

def parse_countries_table(table_tag):
    """
    Looks in the "wikitable" table and takes the information from the columns "Common and formal names", "Membership within the UN System".
    From "Common and formal names" we extract the name and the link.
    From "Membership within the UN System" we see if it's actually a country or not.
    :param table_tag: the table we are searching in
    :return: all the countries found in the table
    """
    body = table_tag.find("tbody")
    tr_s = body.findAll("tr")

    countries = []
    country_name = ""
    link = ""
    membership = ""

    # skip the 3 extra lines from the table
    for tr in tr_s[3: len(tr_s)]:
        if tr.find("span", class_="flagicon"):
            for td in tr.findAll("td")[0: 1]:

                # [0: 1] because some things were acting weird because of the [a-z] links
                for a in td.findAll("a")[0: 1]:

                    # fix names: "Bahamas, The" -> "The Bahamas"
                    if "," in a.text:
                        first = a.text[a.text.find(",") + 2:]
                        second = a.text[0: a.text.find(",")]

                        country_name = first + " " + second
                    else:
                        country_name = a.text

                    link = a.get("href")

            for td in tr.findAll("td")[1: 2]:
                if td.text[0: len("A UN member state")] == "A UN member state":
                    membership = "UN member state"
                elif td.text[0: len("A UN observer state")] == "A UN observer state":
                    membership = "UN observer state"
                else:
                    membership = None

            if membership is None:
                continue

            countries.append((country_name, link))

    # io.open + encoding because i was getting the ERROR:  'charmap' codec can't encode characters
    with io.open("countries.txt", "w", encoding="utf-8") as file:
        for tuple in countries:
            file.write(str(tuple[0]) + ", " + str(tuple[1]))
            file.write("\n")

    file.close()

    return countries


def get_countries(countries_url):
    """
    Crawls https://simple.wikipedia.org/wiki/List_of_countries to get all the countries.
    :param countries_url: https://simple.wikipedia.org/wiki/List_of_countries
    :return: list containing name and link for each country
    """
    page = requests.get(countries_url)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")

    countries = parse_countries_table(table)

    return countries
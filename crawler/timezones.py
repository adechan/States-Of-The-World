import re

import requests
from bs4 import BeautifulSoup

def find_second_occurrence(string, substring):
    """
    Find second occurrence of substring in string
    :param string: a string
    :param substring: a string to look for in the main string
    :return: the index of second occurrence of substring in string
    """
    first_occurrence = string.find(substring)
    return string.find(substring, first_occurrence + 1)

def get_timezones_from_table(td_s):
    """
    We look in the row where we found a match for country name, and we get all timezones
    from the third column found in that row.
    :param td_s: list of all td's where we found a country name match
    :return: list of timezones of the country
    """
    # example: UTC−04:00 (AST)
    r = re.compile("(UTC(\\+|−|±)[0-9][0-9]:[0-9][0-9]( \\([a-zA-Z\\s*]*\\))*)")
    found = re.findall(r, td_s[2].text)

    timezones = []
    for item in found:
        # removing the unofficial ones from the list
        r = re.compile("\\(unofficial\\)")
        if re.findall(r, item[0]):
            continue

        # get rid of everything after first "()"
        if find_second_occurrence(item[0], "(") >= 8:  # 8: ex. UTC+01:00
            index_second_occurrence = find_second_occurrence(item[0], "(")
            timezones.append(item[0][0: index_second_occurrence].strip())

        else:
            timezones.append(item[0])

    return timezones

def get_timezones(country_name):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_time_zones_by_country to get all the timezones
    that a country has.
    :param country_name: name of the country
    :return: list with all the timezones found in that country
    """
    root = "https://en.wikipedia.org/wiki/List_of_time_zones_by_country"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")
    table_body = table.find("tbody")

    timezones = []
    tr_s = table_body.findAll("tr")

    for tr in tr_s:
        td_s = tr.findAll("td")

        if len(td_s) == 0:
            continue

        # fix names: ex. "Korea, North" -> "North Korea"
        if "," in td_s[0].text:
            name_strip = td_s[0].text
            first = name_strip[td_s[0].text.find(",") + 2:]
            second = name_strip[1: td_s[0].text.find(",")]
            name = first.strip() + " " + second.strip()
        else:
            name = td_s[0].text.strip()

        # if we find a match using the full name of country
        # or we find a match skipping "The "
        # then we get the timezones
        if country_name == name or (country_name[4:] == name and len(name) > 4):
            timezones.extend(get_timezones_from_table(td_s))

    # if we didn't find any timezone using the country's name,
    # then we look to see if the table data contains the given country's name
    if len(timezones) == 0:
        for tr in tr_s:
            td_s = tr.findAll("td")
            if len(td_s) == 0:
                continue

            if country_name in td_s[0].text.strip():
                timezones.extend(get_timezones_from_table(td_s))

    return timezones

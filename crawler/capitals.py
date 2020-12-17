import re

import requests
from bs4 import BeautifulSoup

def find_bad_links(tag, td):
    """
    Function used to skip the tags we don't want information from.
    For example span, sup, small tags. They usually have <a> tags, but the information is not needed.
    :param tag: span, sup, small
    :param td: table data in a row
    :return: a_s in the tag, all the tags found
    """
    tags_found = td.findAll(tag)
    links = []
    if len(tags_found) != 0:
        for tag in tags_found:
            for item in tag.findAll("a"):
                links.append(item)

    return links, tags_found

def get_capitals_from_table(td_s):
    """
    We look in the row where we found a match for country name, and we get all capitals
    from the second column found in that row.
    :param td_s: list of all td's where we found a country name match
    :return: list of capitals for that country
    """
    a_s = td_s[1].findAll("a")
    a_small, small_s = find_bad_links("small", td_s[1])

    capitals = []

    for a in a_s:
        if a in a_small and len(small_s) != 0:
            continue

        r = re.compile(">([\\w\\s,.'-]*?)</a>")
        if re.search(r, str(a)) and re.search(r, str(a)).group(1) != "None":
            capital = re.search(r, str(a)).group(1)

            # special case because wikipedia has 2 versions of the same capital:
            # "Sri Jayawardenapura Kotte" (incorrect) and "Sri Jayawardenepura Kotte" (correct)
            # so we just exclude the wrong one.
            if capital != "" and capital.strip() != "Sri Jayawardenapura Kotte":
                capitals.append(capital)

    return capitals

def get_capital(country_name, country_link):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_and_their_capitals_in_native_languages
    and https://en.wikipedia.org/wiki/List_of_countries_with_multiple_capitals to get the capitals for a country.
    :param country_name: name of the country
    :param country_link: link of the country
    :return: list with all the capitals from that country
    """
    root = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_and_their_capitals_in_native_languages"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    tables = body.findAll("table", class_="wikitable")

    capitals = []
    for table in tables:
        table_body = table.find("tbody")
        tr_s = table_body.findAll("tr")

        for tr in tr_s:
            td_s = tr.findAll("td")

            if len(td_s) == 0:
                continue

            for td in td_s:

                # find name of the country
                r_name = re.compile("([a-zA-Z\\s-]*)")
                name = re.search(r_name, str(td.text.strip())).group(0)

                # if we find a match, then we get the capital for that country
                # which is in the same row as the country name
                if name == country_name:
                    capitals.extend(get_capitals_from_table(td_s))

            # if we can't find any capital using the name of the country,
            # then we use the link of the country
            if len(capitals) == 0:
                a_s = td_s[0].findAll("a")
                for a in a_s:
                    link = a.get("href")
                    if link == country_link:
                        capitals.extend(get_capitals_from_table(td_s))

    # Some countries have multiple capitals, so we search in another table to get all capitals
    # which are not found in the first table
    root_multiple_capitals = "https://en.wikipedia.org/wiki/List_of_countries_with_multiple_capitals"
    page = requests.get(root_multiple_capitals)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")

    tr_s = table.findAll("tr")

    for index, tr in enumerate(tr_s):
        td_s = tr.findAll("td")

        for td in td_s:
            if td.text.strip() == country_name:
                # we found the first capital from the row, but we also need the next row
                if td_s[1].text not in capitals:
                    capitals.append(td_s[1].text.strip())

                tr_new = tr_s[index + 1]
                td_s_new = tr_new.findAll("td")

                if td_s_new[0].text.strip() not in capitals:
                    capitals.append(td_s_new[0].text.strip())

    return list(set(capitals))
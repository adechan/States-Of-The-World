import re

import requests
from bs4 import BeautifulSoup

def is_official_language_tr(tr):
    """
    :param tr: current row
    :return: True, if the row contains information about *Official* languages,
             False, otherwise
    """
    th = tr.find('th')
    if th is not None:
        match = re.search("\\s*Official\\s*language(s|\\s*)\\s*", th.text)
        if match is not None:
            return True
    return False

def is_official_national_language_tr(tr):
    """
    :param tr: current row
    :return: True, if the row contains information about *Official and national* languages,
             False, otherwise
    """
    th = tr.find('th')
    if th is not None:
        match = re.search("\\s*Official\\s*language(s|\\s*)\\s*and\\s*national\\s*language(s|\\s*)\\s*", th.text)
        if match is not None:
            return True
    return False

def is_spoken_language_tr(tr):
    """
    :param tr: current row
    :return: True, if the row contains information about *Spoken* languages,
             False, otherwise
    """
    th = tr.find('th')
    if th is not None:
        match = re.search("\\s*Spoken\\s*language(s|\\s*)\\s*", th.text)
        if match is not None:
            return True
    return False

def is_national_language_tr(tr):
    """
    :param tr: current row
    :return: True, if the row contains information about *National* languages,
             False, otherwise
    """
    th = tr.find('th')
    if th is not None:
        match = re.search("\\s*National\\s*language(s|\\s*)\\s*", th.text)
        if match is not None:
            return True
    return False

def find_bad_links(tag, td):
    """
    sup -> has footnotes
    span -> (de facto)...
    small ->
    :param tag: span, sup, small (because they usually have links in their tag, and they are not proper languages)
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

def find_languages_in_tr(tr, *language_types):
    """
    :param tr: the current row
    :param language_types: official, national, spoken
    :return: list of languages of type language_type found in that row
    """
    td = tr.find("td")
    a_s = td.findAll("a")

    while td.find("sup"):
        td.sup.decompose()

    while td.find("small"):
        td.small.decompose

    a_span, span_s = find_bad_links("span", td)

    languages_found = {}

    # if there are <a> tags:
    for a in a_s:
        if a in a_span and len(span_s) != 0:
            continue

        r = re.compile('>([a-zA-Z ,&-]*)\\s*</a>')
        match = re.search(r, str(a))
        if match and match.group(1) != "None":

            for language_type in language_types:
                # creates the key
                if language_type not in languages_found.keys():
                    languages_found[language_type] = [match.group(1)]
                # adds to the key
                else:
                    languages_found[language_type].append(match.group(1))

    # if there is no <a> tag then just get the td.text
    if len(a_s) == 0 and td.text.strip() != "None":

        for language_type in language_types:
            if language_type not in languages_found.keys():
                languages_found[language_type] = [td.text.strip()]
            else:
                languages_found[language_type].append(td.text.strip())

    return languages_found

def get_languages_for_unmatched_countries(country_link):
    """
    Crawls for each country its own wikipedia page to find information about
    *official*, *national*, *spoken* languages.
    :param country_link: link of the country
    :return: dictionary with keys being type of the language (official, national,..)
             and the value being a list of languages
    """
    root = "https://en.wikipedia.org" + country_link
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="geography")

    tr_s = table.findAll("tr")

    languages_found = {}

    # get OFFICIAL languages
    for tr in tr_s:
        if is_official_language_tr(tr):
            languages_found.update(find_languages_in_tr(tr, "official"))

        # OFFICIAL and NATIONAL language
        elif is_official_national_language_tr(tr):
            languages_found.update(find_languages_in_tr(tr, "official", "national"))

    # SPOKEN languages
    for tr in tr_s:
        if is_spoken_language_tr(tr):
            languages_found.update(find_languages_in_tr(tr, "spoken"))

    # NATIONAL language
    for tr in tr_s:
        if is_national_language_tr(tr):
            languages_found.update(find_languages_in_tr(tr, "national"))

    return languages_found

def get_all_languages_for_matched_countries(td, language_type):
    """
    Gets all the languages in a country of type <language_type> from the column data <td>
    :param td: the column data that contains languages of type <language_type>
    :param language_type: ex. "official", "regional", "minority", "national", "spoken"
    :return: dictionary where the key is the <language_type> and the value is a list of languages
    """

    while td.find("sup"):
        td.sup.decompose()

    while td.find("small"):
        td.small.decompose()

    languages_found = {}

    if td.text.strip() != "None":
        # remove everything in parentheses, if there are any
        r = re.compile("\\([\\w\\s,&-]*\\)")
        text = re.sub(r, "", td.text.strip())

        # replace ",", "and" with "\n"
        text = text.replace(",", "\n")
        text = text.replace(" and ", "\n")
        text = text.replace(")", "")
        text = text.replace("(", "")

        # remove everything after \n (because some of them have numbers in <td>)
        r = re.compile("(([\n\r]|^)\\d+[\\w\\s]+)([\r\n]|$)")
        text = re.sub(r, "", text)

        # remove "in ..."
        r = re.compile("(\\sin[\\w\\s]*)")
        text = re.sub(r, "", text)

        languages = []
        if len(text) > 0:
            for language in text.split("\n"):
                if language.strip() not in languages:
                    languages.append(language.strip())

        if language_type not in languages_found.keys():
            languages_found[language_type] = languages
        else:
            languages_found[language_type].append(languages)

    return languages_found

def get_all_languages(country_name, country_link):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory to get
    all the languages in a country. If we can't get languages from here, then we crawl the country's link.
    :return: dictionary where the keys is the <language_type> and the value is a list of languages
    """
    root = "https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_="wikitable")

    table_body = table.find("tbody")
    tr_s = table_body.findAll("tr")

    languages_found = {}
    language_types = ["official", "regional", "minority", "national", "spoken"]

    for tr in tr_s:
        td_s = tr.findAll("td")

        if len(td_s) == 0:
            continue

        r = re.compile("[a-zA-Z -]*")
        country = re.search(r, td_s[0].text.strip()).group(0)

        # if we found match using the name
        if country == country_name or country == country_name[4:]:
            for index, language_type in enumerate(language_types):

                # index + 1 because our list of language types start from 0, but
                # in the table we start looking from the second column (index 1)
                # which means that the column index is greater by one than the index from our list
                if len(td_s) > index + 1:
                    languages_found.update(get_all_languages_for_matched_countries(td_s[index + 1], language_type))


    # there are some countries where we couldn't do a match on the name
    # and the links are not the same as the ones we have saved
    # so we check for their official language in their own link
    if len(languages_found) == 0:
        languages_found.update(get_languages_for_unmatched_countries(country_link))

        # for every language type, other than the ones we found languages for, we add a key of <language_type> with empty list as value
        for language_type in language_types:
            if language_type not in languages_found.keys():
                languages_found[language_type] = []


    return languages_found
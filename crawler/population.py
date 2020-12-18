import requests
from bs4 import BeautifulSoup

def get_population_density_from_table(td_s):
    population = td_s[4].text.strip()
    density = td_s[5].text.strip()
    result = (population, density)

    return result

def get_population_and_density(country_name, country_link):
    """
    Crawls https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population_density to get population
    and density (pop./ km²) for each country.
    :param country_name: name of the country
    :param country_link: link of the country
    :return: tuple (population, density) for the given country
    """
    root = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population_density"
    page = requests.get(root)
    body = BeautifulSoup(page.content, "html.parser")
    table = body.find("table", class_ = "wikitable")

    table_body = table.find("tbody")

    result = tuple()
    tr_s = table_body.findAll("tr")
    for tr in tr_s:
        td_s = tr.findAll("td")

        if len(td_s) == 0:
            continue

        a = td_s[1].find("a")

        # checking if the full name is in the second column
        # or if the name without "The " is in the second column
        if (country_name == td_s[1].text.strip() or country_name[4:] == td_s[1].text.strip()) and td_s[0].text != "–":
            result = get_population_density_from_table(td_s)

        # for the countries that have [a-z0-9] in their name (notes)
        # compare if the text link is same as the name
        elif a and len(a.text) > 0:
            if a.text == country_name:
                result = get_population_density_from_table(td_s)

    # if we didn't find data using the country's name, then we use the country link to find a match
    if len(result) == 0:
        tr_s = table_body.findAll("tr")
        for tr in tr_s:
            td_s = tr.findAll("td")

            if len(td_s) == 0:
                continue

            a = td_s[1].find("a")
            link = a.get("href")
            if link == country_link:
                result = get_population_density_from_table(td_s)

    return result
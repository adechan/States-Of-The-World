import io
import json

import crawler

countries_url = "https://simple.wikipedia.org/wiki/List_of_countries"
countries = crawler.countries.get_countries(countries_url)

def create_json_info_countries(countries):
    """
    {
      country_name: {
        link: "",
        capitals: ["", ""..],
        area: "",
        population: "",
        density: "",
        government: "",
        timezones: ["", ""..],
        neighbours: ["", ""..],
        languages: {
          "official": ["", ""..],
          "regional": ["", ""..],
          "minority": ["", ""..],
          "national": ["", ""..],
          "spoken": ["", ""..]
        }
      }
    }
    """
    info_countries = {}

    for country in countries:
        info_country = {}

        country_name = country[0]
        country_link = country[1]

        capitals = crawler.capitals.get_capital(country_name, country_link)
        area = crawler.area.get_area(country_name, country_link)
        population = crawler.population.get_population_and_density(country_name, country_link)[0]
        density = crawler.population.get_population_and_density(country_name, country_link)[1]
        government = crawler.government.get_government_system(country_name, country_link)
        timezones = crawler.timezones.get_timezones(country_name)
        neighbours = crawler.neighbours.get_neighbours(country_name, country_link, countries)
        languages = crawler.languages.get_all_languages(country_name, country_link)

        info_country["link"] = country_link
        info_country["capitals"] = capitals
        info_country["area"] = area
        info_country["population"] = population
        info_country["density"] = density
        info_country["government"] = government
        info_country["timezones"] = timezones
        info_country["neighbours"] = neighbours
        info_country["languages"] = languages

        info_countries[country_name] = info_country

        with io.open("info_countries.txt", "w", encoding="utf-8") as file_info_countries:
            json.dump(info_countries, file_info_countries, ensure_ascii=False, indent=4)

        print("Done writing information about " + country_name)

    print("Finally done!")



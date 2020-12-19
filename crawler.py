import crawler

countries_url = "https://simple.wikipedia.org/wiki/List_of_countries"
countries = crawler.countries.get_countries(countries_url)

def test_countries_info(countries):
    print("Found information about " + str(len(countries)) + " countries")
    for country in countries:
        country_name = country[0]
        country_link = country[1]

        test_country_info(country_name, country_link)

def test_country_info(country_name, country_link):
    print("============================================================")
    print("Information about -> " + country_name + " - " + country_link + " <-")
    # print("Capital -> " + str(crawler.capitals.get_capital(country_name, country_link)))
    # print("Area -> " + crawler.area.get_area(country_name, country_link))
    # print("Timezones -> " + str(crawler.timezones.get_timezones(country_name)))
    # print("Population -> " + str(crawler.population.get_population_and_density(country_name, country_link)[0]))
    # print("Density -> " + str(crawler.population.get_population_and_density(country_name, country_link)[1]))
    # print("Neighbours -> " + str(crawler.neighbours.get_neighbours(country_name, country_link, countries)))
    print("Form of government -> " + crawler.government.get_government_system(country_name, country_link))



test_countries_info(countries)
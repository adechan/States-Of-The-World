from database import normalization


def normalized_info_country(country_name: str, country_info: dict):
    """
    :param country_name: a country
    :param country_info: dictionary that contains all the information about a country
    :return: name, population, density, area, government
    """
    name = normalization.normalize_text(country_name)
    population = normalization.normalize_numbers(country_info["population"])
    density = normalization.normalize_numbers(country_info["density"])
    area = normalization.normalize_numbers(country_info["area"])
    government = normalization.normalize_text(country_info["government"].replace("\xa0", " "))

    return str(name), str(population), str(density), str(area), str(government)


def get_values_for_countries_table(json: dict):
    """
    Get name, population, density, area, government for each country so we can add it to the database.
    :param json: json that contains all the information about countries
    :return: list of tuples (id, name, population, density, area, government)
    """
    values = []
    i = 1
    for key, value in json.items():
        id = str(i)
        name, population, density, area, government = normalized_info_country(key, value)

        # it doesn't have a form of government
        if government == "n/a":
            government = ""

        values.append((id, name, population, density, area, government))
        i = i + 1

    return values


def insert_into_countries(json):
    sql = "INSERT INTO countries (id, name, population, density, area, government) VALUES (%s, %s, %s, %s, %s, %s)"
    values = get_values_for_countries_table(json)

    return sql, values
from database import normalization

def normalized_info_country(country_info: dict):
    """
    :param country_info: dictionary that contains all the information about a country
    :return: list of capitals from the given dictionary
    """
    capitals = []
    for capital in country_info["capitals"]:
        capitals.append(normalization.normalize_text(capital))

    return capitals


def get_values_for_capitals_table(json: dict):
    """
    Get the capitals for each country so we can add it to the database.
    :param json: json that contains all the information about countries
    :return: list of tuples (id, capital)
    """
    values = []

    i = 1
    for key, value in json.items():
        id = str(i)
        capitals = normalized_info_country(value)

        for capital in capitals:
            values.append((id, capital))

        i = i + 1

    return values


def insert_into_capitals(json):
    sql = "INSERT INTO capitals (id_country, capital) VALUES (%s, %s)"
    values = get_values_for_capitals_table(json)

    return sql, values
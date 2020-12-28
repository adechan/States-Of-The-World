from database import normalization


def get_neighbours_of_a_type(country_info: dict, type: str):
    """
    :param country_info: dictionary that contains all the information about a country
    :param type: type of neighbour (land, maritime)
    :return: list of neighbours of type *type* from the given dictionary
    """
    neighbours_of_type = []

    for key, values in country_info["neighbours"].items():
        if key == type:
            for value in values:
                neighbours_of_type.append(normalization.normalize_text(value))

    return neighbours_of_type

def get_types_neighbours(country_info: dict):
    types = []
    for type in country_info["neighbours"]:
        types.append(type)

    return types

def get_values_for_neighbours_table(json: dict):
    """
    Get the neighbours for each country so we can add it to the database.
    :param json: json that contains all the information about countries
    :return: list of tuples (id, neighbour, type)
    """
    values = []
    types = []

    i = 1
    for key, value in json.items():
        types = get_types_neighbours(value)

        id = str(i)
        for type in types:
            languages = get_neighbours_of_a_type(value, type)

            for language in languages:
                values.append((id, language, type))

        i = i + 1
    return values

def insert_into_neighbours(json):
    sql = "INSERT INTO neighbours (id_country, neighbour, type) VALUES (%s, %s, %s)"
    values = get_values_for_neighbours_table(json)
    return sql, values
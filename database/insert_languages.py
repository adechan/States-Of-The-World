from database import normalization


def get_languages_of_a_type(country_info: dict, type: str):
    """
    :param country_info: dictionary that contains all the information about a country
    :param type: type of language (official, regional, national, minority, spoken)
    :return: list of languages of type *type* from the given dictionary
    """
    languages_of_type = []

    for key, values in country_info["languages"].items():
        if key == type:
            for value in values:
                languages_of_type.append(normalization.normalize_text(value))

    return languages_of_type

def get_types_languages(country_info: dict):
    types = []
    for type in country_info["languages"]:
        types.append(type)

    return types

def get_values_for_languages_table(json: dict):
    """
    Get the languages for each country so we can add it to the database.
    :param json: json that contains all the information about countries
    :return: list of tuples (id, language, type)
    """
    values = []
    types = []

    i = 1
    for key, value in json.items():
        types = get_types_languages(value)

        id = str(i)
        for type in types:
            languages = get_languages_of_a_type(value, type)

            for language in languages:
                values.append((id, language, type))

        i = i + 1
    return values

def insert_into_languages(json):
    sql = "INSERT INTO languages (id_country, language, type) VALUES (%s, %s, %s)"
    values = get_values_for_languages_table(json)
    return sql, values
from database import normalization

def normalized_info_country(country_info: dict):
    """
    :param country_info: dictionary that contains all the information about a country
    :return: list of timezones from the given dictionary
    """
    timezones = []
    for timezone in country_info["timezones"]:
        if type(normalization.normalize_timezone(timezone)) is list:
            for item in normalization.normalize_timezone(timezone):
                timezones.append(item)
        else:
            timezones.append(normalization.normalize_timezone(timezone))

    return timezones


def get_values_for_timezones_table(json: dict):
    """
    Get the timezones for each country so we can add it to the database.
    :param json: json that contains all the information about countries
    :return: list of tuples (id, timezone)
    """
    values = []

    i = 1
    for key, value in json.items():
        id = str(i)
        timezones = normalized_info_country(value)

        for timezone in timezones:
            values.append((id, timezone))

        i = i + 1

    return values

def insert_into_timezones(json):
    sql = "INSERT INTO timezones (id_country, timezone) VALUES (%s, %s)"
    values = get_values_for_timezones_table(json)
    return sql, values
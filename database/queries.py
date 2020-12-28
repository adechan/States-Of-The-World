import mysql.connector

db_connection = mysql.connector.connect(
        host = "localhost",
        user = "root",    # default
        password = "",    # default
        database = "countries-of-the-world"
    )

def get_top_10_countries_by_keyword(db_connection, keyword, type):
    """
    Get top or bottom 10 by a criteria *keyword*.
    :param keyword: population, area, density
    :param type: max (for TOP 10), min (for BOTTOM 10)
    :return: dictionary that have as keys a number to show the order of the top/bottom
             and as values a tuple that contains the country name and the value of *keyword* column
    """
    cursor = db_connection.cursor(buffered=True)
    if type == "max":
        sql = f"SELECT name, {keyword} FROM countries ORDER BY {keyword} DESC;"
    elif type == "min":
        sql = f"SELECT name, {keyword} FROM countries ORDER BY {keyword} ASC;"
    cursor.execute(sql)

    values = cursor.fetchmany(10)
    response = dict()

    i = 0
    for value in values:
        response[i] = tuple(value)
        i += 1

    return response


def get_countries_based_on_government_type(db_connection, type):
    """
    Get all countries that have some given government type.
    :param type: a government type: Republic, Absolute Monarchy, Constitutional Monarchy.
    :return: dictionary that have as keys a number
             and as values a tuple that contains the country name
    """
    cursor = db_connection.cursor(buffered=True)
    sql = f"SELECT name FROM countries WHERE LOWER(government) = LOWER('{type}');"

    cursor.execute(sql)
    values = cursor.fetchall()
    response = dict()

    i = 0
    for value in values:
        response[i] = tuple(value)
        i += 1
    return response


def get_countries_with_no_government(db_connection):
    """
    Get all countries that have no government system.
    """
    cursor = db_connection.cursor(buffered=True)
    sql = "SELECT name FROM countries WHERE government = ''"

    cursor.execute(sql)
    values = cursor.fetchall()
    response = dict()

    i = 0
    for value in values:
        response[i] = tuple(value)
        i += 1
    return response


def get_countries_that_have_the_timezone(db_connection, timezone):
    """
    Get all countries that have some given timezone.
    :param timezone: ex. UTC-02:00, UTC+02:00
    :return: dictionary that have as keys a number
             and as values a tuple that contains the country name, timezone
    """
    cursor = db_connection.cursor(buffered=True)

    sql = "SELECT countries.name, timezones.timezone " \
          "FROM countries " \
          "JOIN timezones ON countries.id = timezones.id_country " \
          f"WHERE LOWER(SUBSTR(timezone, 1, 9)) = LOWER('{timezone}');"

    cursor.execute(sql)
    values = cursor.fetchall()
    response = dict()

    i = 0
    for value in values:
        response[i] = tuple(value)
        i += 1
    return response


def get_countries_that_speak_language(db_connection, language):
    """
    Get all countries that the given language found in any language type (official, national, minority, spoken)
    :param language: ex. english, romanian, spanish
    :return: dictionary that have as keys a number
             and as values a tuple that contains the country name
    """
    cursor = db_connection.cursor(buffered=True)
    sql = "SELECT countries.name " \
          "FROM countries " \
          "JOIN languages ON countries.id = languages.id_country " \
          f"WHERE LOWER(languages.language) = LOWER('{language}');"

    cursor.execute(sql)
    values = cursor.fetchall()
    response = dict()

    i = 0
    for value in values:
        response[i] = tuple(value)
        i += 1
    return response

def get_countries_with_language_of_type(db_connection, language, type):
    """
    Get all countries that have in the given type a given language.
    :param language: ex. romanian
    :param type: ex. official
    :return: dictionary that have as keys a number
             and as values a tuple that contains the country name, language, type
    """
    cursor = db_connection.cursor(buffered=True)
    sql = "SELECT countries.name, languages.language, languages.type " \
          "FROM countries " \
          "JOIN languages ON countries.id = languages.id_country " \
          f"WHERE LOWER(languages.language) = LOWER('{language}') AND LOWER(languages.type) = LOWER('{type}');"

    cursor.execute(sql)
    values = cursor.fetchall()
    response = dict()

    i = 0
    for value in values:
        response[i] = tuple(value)
        i += 1
    return response

def get_info_about_country(db_connection, country):
    """
    Get all information about a given country.
    :return: dictionary that contains id, country name, population, density, area, government, capital, languages, timezones, neighbours
    """
    cursor = db_connection.cursor(buffered=True)
    sql = "SELECT countries.id, countries.name, countries.population, countries.density, countries.area, countries.government, capitals.capital " \
          "FROM countries " \
          "JOIN capitals ON countries.id = capitals.id_country " \
          f"WHERE LOWER(countries.name) = LOWER('{country}');" \

    cursor.execute(sql)
    values = cursor.fetchall()

    id = values[0][0]
    country = values[0][1]
    population = values[0][2]
    density = values[0][3]
    area = values[0][4]
    government = values[0][5]
    capital = values[0][6]

    info_country = [("id", id), ("country", country), ("population", population), ("density", density), ("area", area), ("government", government), ("capital", capital)]

    sql = "SELECT languages.language, languages.type " \
          f"FROM languages WHERE languages.id_country = {id};"

    cursor.execute(sql)
    values = cursor.fetchall()

    languages = {}
    for value in values:
        if value[1] not in languages:
            languages[value[1]] = [value[0]]
        else:
            languages[value[1]].append(value[0])

    info_country.append(("languages", languages))

    sql = "SELECT neighbours.neighbour, neighbours.type " \
          f"FROM neighbours WHERE neighbours.id_country = {id};"

    cursor.execute(sql)
    values = cursor.fetchall()

    neighbours = {}
    for value in values:
        if value[1] not in neighbours:
            neighbours[value[1]] = [value[0]]
        else:
            neighbours[value[1]].append(value[0])

    info_country.append(("neighbours", neighbours))

    sql = "SELECT timezones.timezone " \
          f"FROM timezones WHERE timezones.id_country = {id};"

    cursor.execute(sql)
    values = cursor.fetchall()

    timezones = []
    for value in values:
        timezones.append(value[0])

    info_country.append(("timezones", timezones))

    response = dict()
    for item in info_country:
        if item[0] not in response:
            response[item[0]] = item[1]
        else:
            response[item[0]].append(item[1])

    return response


def get_countries_that_have_multiple_capitals(db_connection):
    """
    Get all countries that have 2+ capitals.
    """
    cursor = db_connection.cursor(buffered=True)
    sql = "SELECT countries.name, capitals.id_country, COUNT(capitals.capital) " \
          "FROM capitals " \
          "JOIN countries ON countries.id = capitals.id_country " \
          "GROUP BY capitals.id_country, countries.name;"

    cursor.execute(sql)
    values = cursor.fetchall()

    found_values = []
    for value in values:
        if value[2] >= 2:
            found_values.append(value)
        else:
            continue

    response = dict()
    for item in found_values:
        if item[2] not in response:
            response[item[2]] = [item[0]]
        else:
            response[item[2]].append(item[0])

    return response

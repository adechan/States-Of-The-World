# python needs a driver to access the database
import mysql.connector
import database

import io
import json

def read_json_info_countries(file):
    with io.open(file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    countries_json = json.dumps(data, indent=4)  # string
    return json.loads(countries_json)            # dictionary

json = read_json_info_countries("info_countries.txt")


db_connection = mysql.connector.connect(
        host = "localhost",
        user = "root",    # default
        password = "",    # default
        database = "countries-of-the-world"
    )

# Insert into countries
cursor = db_connection.cursor()
sql_countries, sql_countries = database.insert_countries.insert_into_countries(json)

# cursor.executemany(sql_countries, sql_countries)
# db_connection.commit()
# print(cursor.rowcount, " was inserted.")

# Insert into capitals
sql_capitals, values_capitals = database.insert_capitals.insert_into_capitals(json)
# cursor.executemany(sql_capitals, values_capitals)
# db_connection.commit()
# print(cursor.rowcount, " was inserted.")

# Insert into timezones
sql_timezones, values_timezones = database.insert_timezones.insert_into_timezones(json)
# cursor.executemany(sql_timezones, values_timezones)
# db_connection.commit()
# print(cursor.rowcount, " was inserted.")

# Insert into languages
sql_languages, values_languages = database.insert_languages.insert_into_languages(json)
# cursor.executemany(sql_languages, values_languages)
# db_connection.commit()
# print(cursor.rowcount, " was inserted.")

# Insert into neighbours
sql_neighbours, values_neighbours = database.insert_neighbours.insert_into_neighbours(json)
# cursor.executemany(sql_neighbours, values_neighbours)
# db_connection.commit()
# print(cursor.rowcount, " was inserted.")
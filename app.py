from flask import Flask, request
from database import queries
import mysql.connector

db_connection = mysql.connector.connect(
        host = "localhost",
        user = "root",    # default
        password = "",    # default
        database = "countries-of-the-world"
    )

app = Flask(__name__)


@app.route('/api/get-top-10', methods = ['GET'])
def get_top_10_by_population():
    criteria = request.args.get('criteria')
    values = queries.get_top_10_countries_by_keyword(db_connection, criteria, "max")
    return values

@app.route('/api/get-bottom-10', methods = ['GET'])
def get_bottom_10_by_population():
    criteria = request.args.get('criteria')
    values = queries.get_top_10_countries_by_keyword(db_connection, criteria, "min")
    return values

@app.route('/api/get-countries-by-government', methods = ['GET'])
def get_countries_by_government_type():
    government = request.args.get('government')
    values = queries.get_countries_based_on_government_type(db_connection, government)
    return values

@app.route('/api/get-countries-with-no-government', methods = ['GET'])
def get_countries_with_no_government():
    values = queries.get_countries_with_no_government(db_connection)
    return values

@app.route('/api/get-countries-by-timezone', methods = ['GET'])
def get_countries_by_timezone():
    timezone = request.args.get('timezone')
    if " " in timezone:
        timezone = timezone.replace(" ", "+")
    values = queries.get_countries_that_have_the_timezone(db_connection, timezone)
    return values

@app.route('/api/get-countries-that-speak', methods = ['GET'])
def get_countries_that_speak_language():
    language = request.args.get('language')
    values = queries.get_countries_that_speak_language(db_connection, language)
    return values

@app.route('/api/get-countries-by-language-and-type', methods = ['GET'])
def get_countries_by_language_and_type():
    language = request.args.get('language')
    type = request.args.get('type')
    values = queries.get_countries_with_language_of_type(db_connection, language, type)
    return values

@app.route('/api/get-info-about-country', methods = ['GET'])
def get_info_about_country():
    country = request.args.get('country')
    values = queries.get_info_about_country(db_connection, country)
    return values

@app.route('/api/get-countries-that-have-multiple-capitals', methods = ['GET'])
def get_countries_that_have_multiple_capitals():
    values = queries.get_countries_that_have_multiple_capitals(db_connection)
    return values

def list_routes():
    routes = []

    for rule in app.url_map.iter_rules():
        if str(rule) == '/' or str(rule) == '/static/<path:filename>':
            continue
        routes.append(str(rule))

    return routes
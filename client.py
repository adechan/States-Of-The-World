import app
import requests
import json

def parse_result(text):
    parsed_result = json.loads(text)
    return json.dumps(parsed_result, indent=4)

def help():
    routes = app.list_routes()
    i = 0
    print("================================================================================================")
    for route in routes:
        print(str(i) + " -> " + route)
        i += 1
    print("================================================================================================")

def client_main():
    print("Welcome to the Countries of the world API.")
    print("================================================================================================")
    print("Here you can find a list of all possible information that you can get using this API.")
    print("Each request has a number attached to it, so if you want to make that request you just need to write the number.")
    print("If you ever forget the requests that you can make, type 'help'.")
    print("If you don't want to do any other requests, type 'exit'.")

    routes = app.list_routes()

    options = []
    i = 0
    print("================================================================================================")
    for route in routes:
        options.append((route, i))
        print(str(i) + " -> " + route)
        i += 1
    print("================================================================================================")

    while True:
        url = "http://127.0.0.1:5000"

        option = input("Write an option: ")
        if option == "help":
            help()
        elif option == "exit":
            break

        else:

            route = str
            for op in options:
                if op[1] == int(option):
                    route = op[0]

            url += route
            if route == "/api/get-countries-by-language-and-type":
                language = input("You need to write a language that you are interested in: ")
                type = input("Choose one between the types of languages: official, national, minority, regional, spoken: ")

                url += f"?language={language}&type={type}"

                result = requests.get(url)
                print(parse_result(result.text))

            elif route == "/api/get-countries-by-government":
                government = input("Choose one between the types of government: republic, absolute monarchy, constitutional monarchy: ")

                url += f"?government={government}"
                result = requests.get(url)
                print(parse_result(result.text))

            elif route == "/api/get-countries-with-no-government":

                result = requests.get(url)
                print(parse_result(result.text))

            elif route == "/api/get-countries-by-timezone":
                timezone = input("Choose a timezone you are interested in (ex. UTC+00:00, UTC-02:00): ")

                url += f"?timezone={timezone}"
                result = requests.get(url)
                print(parse_result(result.text))

            elif route == "/api/get-countries-that-speak":
                language = input("You need to write a language that you are interested in: ")

                url += f"?language={language}"
                result = requests.get(url)
                print(parse_result(result.text))

            elif route == "/api/get-top-10":
                categories = ["population", "density", "area"]
                print("You need to choose one between population, density, area so you receive a top 10 made by the one you have chosen.")

                possibilities = []
                j = 0
                for category in categories:
                    possibilities.append((category, j))
                    print(str(j) + " -> " + category)
                    j += 1

                possibility = int(input("Choose one number that represents the category you want: "))

                criteria = ""
                for po in possibilities:
                    if po[1] == int(possibility):
                        criteria = po[0]

                url += f"?criteria={criteria}"
                result = requests.get(url)
                print(parse_result(result.text))

            elif route == "/api/get-bottom-10":
                categories = ["population", "density", "area"]
                print("You need to choose one between population, density, area so you receive a bottom 10 made by the one you have chosen.")

                possibilities = []
                j = 0
                for category in categories:
                    possibilities.append((category, j))
                    print(str(j) + " -> " + category)
                    j += 1

                possibility = int(input("Choose one number that represents the category you want: "))

                criteria = ""
                for po in possibilities:
                    if po[1] == int(possibility):
                        criteria = po[0]


                url += f"?criteria={criteria}"
                result = requests.get(url)
                print(parse_result(result.text))

            elif route == "/api/get-info-about-country":
                country = input("Type one country: ")

                url += f"?country={country}"
                result = requests.get(url)
                print(parse_result(result.text))

            elif route == "/api/get-countries-that-have-multiple-capitals":

                result = requests.get(url)
                print(parse_result(result.text))

client_main()

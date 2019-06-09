import requests.exceptions as Error
import requests

API_KEY = "e642d8c438804deab5741155170507"
CORE_URL = "http://api.apixu.com/v1/"
PATH_FOR_CURRENT = CORE_URL + "current.json?key=" + API_KEY
PATH_FOR_FORECAST = CORE_URL + "forecast.json?key=" + API_KEY
data = {}


# gets integer, prompting retry on invalid input
def get_int(notif):
    number = input(notif)
    while (number.isdigit() == False):
        number = input("Please input a valid choice:  ")
    return int(number)


# gets extra options for forecast request
def get_forecast_options():
    days = get_int("How many days in the future are we looking?(1~10): ")
    while days > 10 or days < 1:
        days = get_int("We can only look 1~10 days in the future :(: ")
    return {"days": days}


def run(where='Kampala', when=1, how_many=2):
    where = 'Kampala' if where is 'here' else where

    city = where

    data["q"] = city

    pref = when

    if pref is 2:
        data.update({"days": how_many})

    pref = PATH_FOR_FORECAST if pref is 2 else PATH_FOR_CURRENT

    print("Getting weather forecast for " + city + "...")

    try:
        reply = requests.get(pref, params=data)
    except Error.ConnectionError as e:
        return "Couldn't find records for " + city

    if not reply.status_code == requests.codes.ok:
        return "Couldn't find records for " + city

    reply = (reply.json())["current"] if pref is PATH_FOR_CURRENT else \
        (reply.json())["forecast"]["forecastday"]  # extract current object

    if pref is PATH_FOR_CURRENT:
        return (city + " is " + reply["condition"]["text"] + " today, at " + str(
            reply["temp_c"]) + " degrees. " + "It feels like " + str(
            reply["feelslike_c"]) + " degress though!")
    else:
        message = ''
        for day in range(0, data["days"]):
            message = message + ("Tomorrow, " if day is 0 else "Then the next day, ")
            message = message + city + " will be " + reply[day]["day"]["condition"][
                "text"] + ", at " + str(
                reply[day]["day"]["avgtemp_c"]) + " degrees on average. "
        return message

if __name__ == "__main__":
    print(run())

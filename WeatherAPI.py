import datetime as dt
import requests
from datetime import date

URL_PAST="https://archive-api.open-meteo.com/v1/archive?"
URL_FUTURE="https://api.open-meteo.com/v1/forecast?"
LAT="52.52"
LONG="13.41"
START="2023-03-30"
END="2023-04-13"
TEMP="temperature_2m"
TODAY = date.today()
urlPast=URL_PAST+"latitude="+LAT+"&longitude="+LONG+"&start_date="+START+"&end_date="+END+"&hourly="+TEMP
urlFuture=URL_FUTURE+"latitude="+LAT+"&longitude="+LONG+"&hourly="+TEMP
responsePast = requests.get(urlPast).json()
responseFuture = requests.get(urlFuture).json()


print(responseFuture["hourly"]["time"])
print()
print(responsePast["hourly"]["time"])



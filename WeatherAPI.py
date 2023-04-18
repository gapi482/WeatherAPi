import datetime as dt
import requests
from datetime import date
from geopy.geocoders import Nominatim
from dateutil.relativedelta import relativedelta 
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
import geocoder

URL_PAST="https://archive-api.open-meteo.com/v1/archive?"
URL_FUTURE="https://api.open-meteo.com/v1/forecast?"
LAT="52.52"
LONG="13.41"
START="2023-03-30"
END="2023-04-13"
TEMP="temperature_2m"
TODAY = date.today()




def main():
    urlPast=URL_PAST+"latitude="+LAT+"&longitude="+LONG+"&start_date="+START+"&end_date="+END+"&hourly="+TEMP
    urlFuture=URL_FUTURE+"latitude="+LAT+"&longitude="+LONG+"&hourly="+TEMP

    responsePast = requests.get(urlPast).json()
    responseFuture = requests.get(urlFuture).json()

    mode= input("Set mode(1 - Set location; 2 - My location; 3 - Past weather):")
    if mode=="1":
        responseFuture=Location(responseFuture)
        ShowData(responseFuture)
    elif mode=="2":
        responseFuture=MyLocation(responseFuture)
        ShowData(responseFuture)
    elif mode=="3":
        responsePast=RealTime(responsePast)
        ShowData(responsePast)
    else:
        print("Predifened parameters")
        ShowData(responseFuture)





def Location(urlFuture):
    geoLocator = Nominatim(user_agent="MyApp")
    location = input("Enter Location:")
    Location = geoLocator.geocode(location)
    print("The latitude of the location is: ", Location.latitude)
    print("The longitude of the location is: ", Location.longitude)
    LAT=str(Location.latitude)
    LONG=str(Location.longitude)

    urlFuture=URL_FUTURE+"latitude="+LAT+"&longitude="+LONG+"&hourly="+TEMP
    responseFuture = requests.get(urlFuture).json()
    return(responseFuture)

def MyLocation(urlFuture):
    g = geocoder.ip('me')
    print(g.latlng)
    LAT=str(g.latlng[0])
    LONG=str(g.latlng[1])
    
    urlFuture=URL_FUTURE+"latitude="+LAT+"&longitude="+LONG+"&hourly="+TEMP
    responseFuture = requests.get(urlFuture).json()
    return(responseFuture)


def RealTime(urlPast):
    START=TODAY-relativedelta(days=7)
    urlPast=URL_PAST+"latitude="+LAT+"&longitude="+LONG+"&start_date="+str(START)+"&end_date="+str(TODAY)+"&hourly="+TEMP
    responsePast = requests.get(urlPast).json()
    return(responsePast)


def ShowData(data):
    # date="" noče zaznati ure da bi samo vsako 12to izbral in nato pokazal
    # a=0
    # for i in past["hourly"]["time"]:
    #     if i[11:13] == 12 or i[11:13] == 00:
    #         date[a]=i
    #         a+=1

    plt.plot(data["hourly"]["time"],data["hourly"]["temperature_2m"])
    plt.xlabel('Time')
    plt.ylabel('Temperature')

    plt.title('Past weather')

    plt.legend()
    plt.show()
    
    
if __name__ == "__main__":
    main()
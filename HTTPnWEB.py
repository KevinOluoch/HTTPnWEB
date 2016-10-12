import unirest
import json


def get_forecast(latitude, longitude):
    """ A function that retrives data on weather forecast for a given location
    given its Latitude and longitude
    """
    print "Fetching updates from server...."
    response = unirest.get(
    "https://simple-weather.p.mashape.com/weatherdata?lat=%f&lng=%f" %(float(latitude), float(longitude)),
    headers={
    "X-Mashape-Key": "6T6fbcjHG2mshPlCVQbgLnA69gyEp1eusEsjsnut1L0zzyWLuD",
    "Accept": "application/json"
    }
    )
    if response.code ==200:
        print "Update fetching from server successful"
    else:
        return "Sorry, the server request was unsuccessful Error code: " + response.code
    for word in ("results",'"forecast":[{"'):
        try:
            response1 = response.raw_body.split(word,1)[1]
        except IndexError:
            return 0


    response1 = response1.split('}],"description"',1)[0]
    response1 = response1.split("},{")
    week_data = {}
    i=0
    for day_weather in response1:

        day_weather=day_weather.split(",")

        day_data = {}
        for data in day_weather:

            data = data.split(':')
            day_data[data[0]] = data[1]
        week_data[i] = day_data
        i+=1
    return week_data


def weather_forecast(day, week_data):
    """ A function that checks the weather for a particular day"""
    if not (day in ("Today", "Mon","Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
        return 0
    else:
        if day == 'Today':
            indx = 0
        else:
            d = 1
            while d < 8:
                print week_data[d]['"day"']
                if week_data[d]['"day"'][1:-1] == day:
                    indx = d
                d += 1
        return "The forecast for %s is: '%s' with Tempreture (High : %s, Low : %s)" %(day, week_data[indx]['"text"'], week_data[indx]['"high"'], week_data[indx]['"low"'])


def main():
    goodbye = False
    while True:
        print "WELCOME TO THE WEATHER APP, THAT GIVES YOU THE WEATHER FORECAST FOR ANY LOCATION GIVEN ITS NOTHING AND EASTING"
        print ("PLEASE INPUT THE LATITUDE AND LONGITIDE OF THE LOCATION YOU WANT FORECAST FOR")
        latitude = raw_input("INPUT THE LATITUDE: Positive number for north and nevative for south")
        longitude = raw_input("INPUT THE LONGITUDE: Positive for east and negative for west")
        for element in (latitude, longitude):
            try:
                float(element)
            except ValueError:
                continue

        if get_forecast(latitude, longitude):
            week_data = get_forecast(latitude, longitude)
        else:
            print "THERE IS NOT WEATHER DATA FOR THAT LOCATION: PLEASE ENTER ANOTHER LOCATION"
            continue

        print "Weather updates ready for use"
        while True:
            day = raw_input("ENTER A DAY TO FORECAST? PLEASE REPLY WITH: Today, Mon,Tue, Wed, Thu, Fri, Sat, OR Sun")
            if  weather_forecast(day, week_data):
                print weather_forecast(day, week_data)
            end = raw_input ("PRESS 0 TO EXIT, 1 TO RE-UPDATE WEATHEER DATA OR ANY KEY TO GET FORECAST FOR ANOTHER DAY")
            if '0' == end:
                goodbye == False
                break
            elif end == '1':
                break
            else:
                pass
        if not goodbye:
            break




if __name__ == '__main__':
    main()





from bs4 import BeautifulSoup
from datetime import datetime, date, time, timedelta
import json
import config
import requests


# Download weather data from the buienradar api
# Return the region of the weather station and the sun intensity
def get_sun_intensity(city_id):
    url = "https://api.buienradar.nl/"
    content = BeautifulSoup(requests.get(url).text, "lxml")
    filtered_content = content.find(id=city_id)
    station_name = filtered_content.stationnaam["regio"]
    intensity = filtered_content.zonintensiteitwm2.string

    if intensity == "-":
        intensity = 0

    return station_name, int(intensity)


# Retrieve the time that of sunrise and sunset
def get_sunrise_sunset():
    url = "https://weather.cit.api.here.com/weather/1.0/report.json?product=forecast_astronomy&name=Eindhoven&app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg"
    content = json.loads(requests.get(url).text)

    sunrise = content["astronomy"]["astronomy"][1]["sunrise"]
    sunrise = datetime.strptime(sunrise, '%I:%M%p').time()

    sunset = content["astronomy"]["astronomy"][1]["sunset"]
    sunset = datetime.strptime(sunset, '%I:%M%p').time()

    return sunrise, sunset


# Calculate the brightness of the bulbs
def calc_sun_based_light_intensity(sun_intensity):
    light_off_treshold = 150

    # Calculate brightness of lights based on the intensity of the sun
    if sun_intensity > light_off_treshold:
        percentage = 0
    else:
        percentage = (1/(0.06*sun_intensity+1))

    return int(254 * percentage)


def calc_time_based_intensity(room, sunrise, sunset, wakeup_time, bedtime):
    current_time = datetime.now().time()
    wakeup_min_thirty = (datetime.combine(date.today(), wakeup_time) - timedelta(minutes=30)).time()

    # Calculate light intensity based on the time of day
    print(room)
    if room == "living_room":
        if current_time < bedtime:
            print("Do nothing to living room lights")
        elif sunset < current_time < bedtime:
            print("Dim the lights slowly")

    if room == "bedroom":
        if wakeup_min_thirty < current_time < wakeup_time:
            print("Gradually turn lights on")


def test():
    city_name, sun_intensity = get_sun_intensity(config.city_id)
    print("City, sun_intensity:", city_name, sun_intensity)

    sunrise, sunset = get_sunrise_sunset()
    print("Sunrise, sunset:", sunrise, sunset)

    light_intensity = calc_sun_based_light_intensity(150)
    print("Light intensity:", light_intensity)

    calc_time_based_intensity("living_room", sunrise, sunset, config.wakeup_time, config.bedtime)
    calc_time_based_intensity("bedroom", sunrise, sunset, config.wakeup_time, config.bedtime)


if __name__ == "__main__":
    test()

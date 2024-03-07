import requests
import json
from dataclasses import dataclass

@dataclass
class Coordinates:
    lat: int
    long: int

class Address:
    def __init__(self, street: str, city: str, state: str, zip: int | str):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
    
    def get_coordinates(self) -> Coordinates:
        try:
            url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={self.street}&city={self.city}&state={self.state}&zip={self.zip}&benchmark=2020&format=json"
            response = requests.get(url)
            geo_location = response.json()
            coordinates = geo_location['result']['addressMatches'][0]['coordinates']
            return Coordinates(lat=coordinates['y'], long=coordinates['x'])
        except Exception:
            print("ERROR: Invalid address entered, unable to get coordinates")
    
    def _get_all_weather_information(self, coordinates: Coordinates) -> json:
        try:
            url = f"https://api.weather.gov/points/{coordinates.lat},{coordinates.long}"
            response = requests.get(url=url)
            weather_data = response.json()
            return weather_data
        except Exception:
            print("ERROR: Invalid lat/long coordinates entered, unable to get weather information")

class WeatherInformation:
    def __init__(self, address: Address):
        self.address = address
        self.all_weather_data = self.address._get_all_weather_information(address.get_coordinates())
        if self.all_weather_data != None:
            _current_forecast_url = self.all_weather_data['properties']['forecastHourly']
            _weather_forecast = requests.get(url=_current_forecast_url).json()
            self.current_weather = _weather_forecast['properties']['periods'][0]
        else:
            self.current_weather = {"temperature": "unknown", "windSpeed":"unknown", "shortForecast":"unknown"}
    
    @property    
    def current_temperature(self):
        return self.current_weather['temperature']

    @property
    def current_wind_speed(self):
        return self.current_weather['windSpeed']
    
    @property
    def current_weather_condition(self):
        return self.current_weather['shortForecast']
    
    @property
    def current_clothing_recommendation(self):
        weather_condition = self.current_weather_condition
        if weather_condition != "unknown":
            is_sunny = True if "sun" in weather_condition.lower() else False
            return f"Wear shorts, the weather condition is {weather_condition}" if is_sunny else f"Wear long pants! The current weather condition is {weather_condition}"
        return "Unable to get weather data, weather condition is unknown"

def main():
    my_current_addreess = Address("937 Westridge Dr","Saint George","UT",84770)
    my_current_address_weather_info = WeatherInformation(my_current_addreess)

    my_previous_address = Address("27932 Kelley Johnson Pkwy", "Santa Clarita", "CA", 91355)
    my_previous_address_weather_info = WeatherInformation(my_previous_address)


    current_address_current_temp = my_current_address_weather_info.current_temperature
    current_address_current_wind_speed = my_current_address_weather_info.current_wind_speed
    current_address_current_weather_condition = my_current_address_weather_info.current_weather_condition
    current_address_current_clothing_recommendation = my_current_address_weather_info.current_clothing_recommendation

    previous_address_current_temp = my_previous_address_weather_info.current_temperature
    previous_address_current_wind_speed = my_previous_address_weather_info.current_wind_speed
    previous_address_current_weather_condition = my_previous_address_weather_info.current_weather_condition
    previous_address_current_clothing_recommendation = my_previous_address_weather_info.current_clothing_recommendation

    print()
    print(f"The current temperature at my current location is {current_address_current_temp} degrees Farenheit.")
    print(f"The current wind speed at my current location is {current_address_current_wind_speed}.")
    print(f"The current weather condtion at my current location is {current_address_current_weather_condition}.")
    print(f"The current clothing recommendation at my current location is {current_address_current_clothing_recommendation}.")

    print()
    print(f"The current temperature at my previous location is {previous_address_current_temp} degrees Farenheit.")
    print(f"The current wind speed at my previous location is {previous_address_current_wind_speed}.")
    print(f"The current weather condtion at my previous location is {previous_address_current_weather_condition}.")
    print(f"The current clothing recommendation at my previous location is {previous_address_current_clothing_recommendation}.")

if __name__ == "__main__":
    main()
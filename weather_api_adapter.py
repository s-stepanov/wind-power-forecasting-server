import requests
import json
import numpy
from arrow import now

class WeatherApiAdapter:

  def __init__(self):
    self.api_url = 'https://api.stormglass.io/v2/weather/point'
    self.api_key = 'cc436780-a274-11ea-a824-0242ac130002-cc436852-a274-11ea-a824-0242ac130002' # TODO Move to environment variavles

  def get_test_weather_data(self):
    weather_data = {}

    with open('test.json') as json_file:
      weather_data = json.load(json_file)

    transformed = self.transform_data(weather_data)

    return transformed


  def get_weather_by_coordinates(self, longtitude, latitude):
    # Get first hour of today
    start = now().floor('day')

    # Get last hour of today
    end = now().ceil('day')

    response = requests.get(
      'https://api.stormglass.io/v2/weather/point',
      params={
        'lat': latitude,
        'lng': longtitude,
        'params': ','.join(['windSpeed50m', 'windDirection50m']),
        'start': start.to('UTC').timestamp,  # Convert to UTC timestamp
        'end': end.to('UTC').timestamp  # Convert to UTC timestamp
      },
      headers={
        'Authorization': self.api_key
      }
    )

    json_data = response.json()
    return json_data


  def transform_data(self, json_data):
    transformed = []

    for row in json_data['hours']:
      transformed.append({
        'time': row['time'],
        'wind_speed': row['windSpeed50m']['noaa'],
        'wind_direction': row['windDirection50m']['noaa']
      })

    return transformed

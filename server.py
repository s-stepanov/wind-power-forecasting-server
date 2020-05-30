from flask import Flask
from flask_cors import CORS

from weather_api_adapter import WeatherApiAdapter
from wind_prediction_net import predict

import json

app = Flask(__name__)
CORS(app)

weatherAdapter = WeatherApiAdapter()

@app.route('/predict')
def get_prediction():
  prediction_data = weatherAdapter.get_test_weather_data()
  
  return {
    'data': predict(prediction_data)
  }


@app.route('/weather')
def get_weather():
  longtitude = -7.881213
  latitude = 43.354377
  return weatherAdapter.get_weather_by_coordinates(longtitude, latitude)


@app.route('/wind-data')
def get_wind_data():
  with open('wind_data.json') as wind_file:
    return json.load(wind_file)
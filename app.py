import requests
import json
from flask import Flask, request, jsonify, abort,render_template, redirect, url_for

api_key = 'ZzA647LQVnhapLTMZePDwaKx7anbyaln'
url_rey_loc = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
lon_lat_start = '55.768740,37.588835'
lon_lat_end = '55.768740, 37.588835'
# 43.223855, 31.727244 - координаты
def find_key_loc(lon_lat):
  param1={'apikey': api_key, 'q': lon_lat , 'language':'ru-ru'}
  response = requests.get(f'{url_rey_loc}',params=param1).json()
  return response['Key']

def get_weather_by_loc(lon_lat_1):
  param2={'apikey': api_key ,'language':'ru-ru', 'details':'true', 'metric':'true'}
  response = requests.get(f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{find_key_loc(lon_lat_1)}', params=param2).json()
  temp = response[0]['Temperature']['Value']
  wind_speed = response[0]['Wind']["Speed"]['Value']
  humidity = response[0]["RelativeHumidity"]
  rain_prob = response[0]["RainProbability"]
  snow_prob = response[0]['SnowProbability']
  UVIndex = response[0]['UVIndex']
  return {'temp': temp,
           'wind_speed': wind_speed,
           'humidity': humidity,
           'rain_prob': rain_prob,
           'snow_prob': snow_prob,
           'UVIndex' : UVIndex,
          'coords':lon_lat_1}




def good_weather(weather):
  if weather['temp']< 0 or  weather['temp']> 35 or weather['wind_speed']> 50 or  weather['rain_prob']> 70 \
          or weather['snow_prob'] >= 70 or weather['UVIndex']>5:
    return 'Погода в данной точке плохая'
  return 'Погода в данной точке хорошая'


app = Flask(__name__)

@app.route('/', methods=['post','get'])
def start_end():
  if request.method == 'POST':
    start = request.form['start']
    end = request.form['end']
    return redirect(url_for('weather', start=start, end=end))
  return render_template('post-form.html')

@app.route('/weather/<start>/<end>')
def weather(start, end):
  try:
    start_weather = get_weather_by_loc(start)
  except:
    mes = {'mes': 'начальной точки'}
    return render_template('erroe_coord.html', mes=mes)
  try:
    end_weather = get_weather_by_loc(end)
  except:
    mes = {'mes': 'конечной точки'}
    return render_template('erroe_coord.html', mes=mes)

  weather_info = {'start': start_weather, 'end': end_weather}
  weather_info['start']['weather'] = good_weather(start_weather)
  weather_info['end']['weather'] = good_weather(end_weather)
  return render_template('weather_start_end.html', weather=weather_info)


if __name__ == '__main__':
  app.run(debug=True)

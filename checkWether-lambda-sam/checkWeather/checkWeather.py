# coding: UTF-8

import logging
import requests
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info('Event: %s', context)

    APIKEY = os.getenv('APIKEY')
    BASEURL = os.getenv('BASEURL')
    PARAM = os.getenv('PARAM')

    url = BASEURL + PARAM + APIKEY
    r = requests.get(url).json()

    logger.info('Event: %s', str(r))
    
    if('wind_gust' not in r) :
      strWeather ={"temp": str(r["current"]["temp"]), "humidity": str(r["current"]["humidity"]), \
        "time": str(r["current"]["dt"]), "feels_like": str(r["current"]["feels_like"]), \
        "pressure": str(r["current"]["pressure"]), "dew_point": str(r["current"]["dew_point"]), \
        "uvi": str(r["current"]["uvi"]), "wind_speed": str(r["current"]["wind_speed"]), \
        "wind_deg": str(r["current"]["wind_deg"]), \
        "weather": r["current"]["weather"][0]["description"] }
    elif('wind_gust' in r) :
      strWeather ={"temp": str(r["current"]["temp"]), "humidity": str(r["current"]["humidity"]), \
        "time": str(r["current"]["dt"]), "feels_like": str(r["current"]["feels_like"]), \
        "pressure": str(r["current"]["pressure"]), "dew_point": str(r["current"]["dew_point"]), \
        "uvi": str(r["current"]["uvi"]), "wind_speed": str(r["current"]["wind_speed"]), \
        "wind_deg": str(r["current"]["wind_deg"]), "wind_gust": str(r["current"]["wind_gust"]), \
        "weather": r["current"]["weather"][0]["description"] }

    return strWeather
    
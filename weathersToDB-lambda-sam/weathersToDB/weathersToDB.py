import json
import datetime
import logging
import psycopg2
import os
import shutil

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Event: %s', event)

    temp = event['temp']
    humidity = event['humidity']
    time = event['time']
    time = datetime.datetime.fromtimestamp(int(time))
    feels_like = event['feels_like']
    pressure = event['pressure']
    dew_point = event['dew_point']
    uvi = event['uvi']
    wind_speed = event['wind_speed']
    wind_deg = event['wind_deg']
    wind_gust = event['wind_gust']
    weather = event['weather']

    #connect
    db_connect = os.getenv('db_connect')
    logger.info('json db_connect %s', db_connect)

    conn = psycopg2.connect(db_connect)
    logger.info('connected')
    #Open a cursor to perform database operations
    cur = conn.cursor()

    sqlstring = "INSERT INTO weathers ( \
        temp, humidity, time, feels_like, pressure, dew_point, uvi, wind_speed, wind_deg, wind_gust, weather, created_at, created_by, updated_at, updated_by) \
        values ('" + str(temp) + "', '" + str(humidity) + "', '" + str(time) + "', '" + str(feels_like) + "', '" + str(pressure) + "', '" + str(dew_point) + \
        "', '" + str(uvi) + "', '" + str(wind_speed) + "', '" + str(wind_deg) + "', '" + str(wind_gust) + "', '" + str(weather) + \
        "', CURRENT_TIMESTAMP, 'OpenWeather', CURRENT_TIMESTAMP, 'OpenWeather');" 
    logger.info('sqlstring: %s', sqlstring)
    cur.execute(sqlstring)
    
    #Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()
    logger.info('conn close.')
        
    return
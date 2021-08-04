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

    nowtimestamp = event['nowtimestamp']
    latitude = event['latitude']
    longitude = event['longitude']
    horizontalAccuracy = event['horizontalAccuracy']
    floorLevel = event['floorLevel']
    altitude = event['altitude']
    PHONE_NAME = event['PHONE_NAME']

    #connect
    db_connect = os.getenv('db_connect')
    logger.info('json db_connect %s', db_connect)

    conn = psycopg2.connect(db_connect)
    logger.info('connected')
    #Open a cursor to perform database operations
    cur = conn.cursor()

    sqlstring = "INSERT INTO locations (time, latitude, longitude, horizontalaccuracy, floorlevel, altitude, created_at, created_by, updated_at, updated_by) values ('" + str(nowtimestamp) + "', '" + str(latitude) + "', '" + str(longitude) + "', '" + str(horizontalAccuracy) + "', '" + str(floorLevel) + "', '" + str(altitude) + "', CURRENT_TIMESTAMP, '" + str(PHONE_NAME) + "', CURRENT_TIMESTAMP, '" + str(PHONE_NAME) + "');" 
    logger.info('sqlstring: %s', sqlstring)
    cur.execute(sqlstring)
    
    #Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()
    logger.info('conn close.')
        
    return
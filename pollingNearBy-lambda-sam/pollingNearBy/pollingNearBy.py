import json
import datetime
import logging
import psycopg2
import os
import shutil

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Event: %s', event)

    #connect
    db_connect = os.getenv('db_connect')
    logger.info('json db_connect %s', db_connect)

    conn = psycopg2.connect(db_connect)
    logger.info('connected')
    #Open a cursor to perform database operations
    cur = conn.cursor()

    sqlstring = "select * from locations order by updated_at desc limit 1;" 
    logger.info('sqlstring: %s', sqlstring)
    cur.execute(sqlstring)
    row = cur.fetchone()
    logger.info('row: %s', row)

    checkRange = []
    checkRange.append(os.getenv('luLati'))
    checkRange.append(os.getenv('luLong'))
    checkRange.append(os.getenv('loLati'))
    checkRange.append(os.getenv('loLong'))
    checkRange.append(os.getenv('roLati'))
    checkRange.append(os.getenv('roLong'))
    checkRange.append(os.getenv('ruLati'))
    checkRange.append(os.getenv('ruLong'))
    print(checkRange)

    point = Feature(geometry=Point((float(row[2]), float(row[3]))))
    polygon = Polygon([[
        (float(checkRange[0]),float(checkRange[1])),
        (float(checkRange[2]),float(checkRange[3])),
        (float(checkRange[4]),float(checkRange[5])),
        (float(checkRange[6]),float(checkRange[7]))
    ]])

    if boolean_point_in_polygon(point, polygon):
        print('領域内')
    else:
        print('領域外')


    # sqlstring = "INSERT INTO locations (lid, location_status, created_at, created_by, updated_at, updated_by) values ('" \
    #  + str(row) + "', '" + str(locationStatus) + "', CURRENT_TIMESTAMP, '" + str(PHONE_NAME) + "', CURRENT_TIMESTAMP, '" + str(PHONE_NAME) + "');" 
    # logger.info('sqlstring: %s', sqlstring)
    # cur.execute(sqlstring)

    #Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()
    logger.info('conn close.')
        
    return
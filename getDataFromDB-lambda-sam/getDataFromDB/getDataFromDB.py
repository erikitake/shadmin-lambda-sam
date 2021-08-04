import logging
import json
import boto3
import urllib.parse
import os
import psycopg2
from datetime import datetime, timedelta, timezone

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

    ident = event["ident"]
    fromDate = event["fromDate"]
    toDate = event["toDate"]
    tableName = event["tableName"]
    targetName = event["targetName"]

    if ident == "temp":
        sqlstring = "select degree, timezone('JST', updated_at::timestamptz) as updated_at from " \
          + str(tableName) + " where updated_at between timezone('JST', '" + str(fromDate) + "'::timestamp) and timezone('JST', '" \
          + str(toDate) + "'::timestamp) and created_by = '" + str(targetName) + "';" 
    if ident == "gps":
        targetNameArray = targetName.split(":")
        sqlstring = "select timezone('JST', time::timestamptz) as time, latitude, longitude, updated_by from " \
          + str(tableName) + " where updated_at between timezone('JST', '" + str(fromDate) + "'::timestamp) and timezone('JST', '" + str(toDate) + "'::timestamp)" 
        for index, elem in enumerate(targetNameArray):
            if index == 0:
                sqlstring = sqlstring + " and ( updated_by = '" + str(elem) + "'"
            else:           
                sqlstring = sqlstring + " or updated_by = '" + str(elem) + "'"
        sqlstring = sqlstring + ") order by updated_at desc limit 2;"
    if ident == "weather":
        sqlstring = "select temp, humidity, pressure, timezone('JST', updated_at::timestamptz) as updated_at from " \
          + str(tableName) + " where updated_at between timezone('JST', '" + str(fromDate) + "'::timestamp) and timezone('JST', '" + str(toDate) + "'::timestamp);" 
 
    logger.info('sqlstring: %s', sqlstring)
    cur.execute(sqlstring)
    rows = cur.fetchall()
    logger.info('rows: %s', rows)
    
    jsonobj = {str(tableName): []}
    if ident == "temp":
        for index, row in enumerate(rows):
            addDict = {"degree": str(row[0]), "datetime": str(row[1])}
            jsonobj[str(tableName)].append(addDict)
    if ident == "gps":
        for index, row in enumerate(rows):
            addDict = {"updated_by": str(row[3]), "latitude": str(row[1]), "longitude": str(row[2]), "time": str(row[0])}
            jsonobj[str(tableName)].append(addDict)
    if ident == "weather":
        for index, row in enumerate(rows):
            addDict = {"temp": str(row[0]), "humidity": str(row[1]), "pressure": str(row[2]), "datetime": str(row[3])}
            jsonobj[str(tableName)].append(addDict)
        
    #Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()
    logger.info('conn close.')
        
    return jsonobj
    
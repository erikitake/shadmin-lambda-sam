import logging
import json
import boto3
import urllib.parse
import os
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client('ssm')
    
def lambda_handler(event, context):
    logger.info('Event: %s', event)

    identiName = event['identiName']
    tedegree = event['tedegree']
    tedatetime= event['tedatetime']
    hudegree= event['hudegree']
    hudatetime= event['hudatetime']
    ildegree= event['ildegree']
    ildatetime= event['ildatetime']

    #connect
    db_connect = os.getenv('db_connect')

    logger.info('json db_connect %s', db_connect)
    conn = psycopg2.connect(db_connect)
    logger.info('connected')
    #Open a cursor to perform database operations
    cur = conn.cursor()
#    sqlstring = "INSERT INTO temperatures (degree, time, created_at, created_by, updated_at, updated_by) values (" + str(tedegree) + ", ('" + str(tedatetime) + "') at time zone 'JST', CURRENT_TIMESTAMP, 'nr', CURRENT_TIMESTAMP, 'nr');" 

    if (tedegree != ''):
        sqlstring = "INSERT INTO temperatures (degree, time, created_at, created_by, updated_at, updated_by) values (" + str(tedegree) + ", '" + str(tedatetime) + "', CURRENT_TIMESTAMP, '" + str(identiName) + "', CURRENT_TIMESTAMP, '" + str(identiName) + "');" 
        logger.info('sqlstring: %s', sqlstring)
        cur.execute(sqlstring)

    if (hudegree != ''):
        sqlstring = "INSERT INTO humiditys (degree, time, created_at, created_by, updated_at, updated_by) values (" + str(hudegree) + ", '" + str(hudatetime) + "', CURRENT_TIMESTAMP, '" + str(identiName) + "', CURRENT_TIMESTAMP, '" + str(identiName) + "');"
        logger.info('sqlstring: %s', sqlstring)
        cur.execute(sqlstring)

    if (ildegree != ''):
        sqlstring = "INSERT INTO illuminances (degree, time, created_at, created_by, updated_at, updated_by) values (" + str(ildegree) + ", '" + str(ildatetime) + "', CURRENT_TIMESTAMP, '" + str(identiName) + "', CURRENT_TIMESTAMP, '" + str(identiName) + "');"
        logger.info('sqlstring: %s', sqlstring)
        cur.execute(sqlstring)

    #Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()
    logger.info('conn close.')

    return
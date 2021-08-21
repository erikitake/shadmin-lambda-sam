import json
import logging
import psycopg2
import os
import shutil
from datetime import datetime, timedelta, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Event: %s', event)

    db_connect = os.getenv('db_connect')
    logger.info('json db_connect %s', db_connect)
    conn = psycopg2.connect(db_connect)
    logger.info('connected')
    cur = conn.cursor()

    roomName= event['roomName']
    checkDegree= event['checkDegree']

    dt_now = datetime.now()
    nowMonth = dt_now.strftime('%m')

    sqlstring = "select degree from " + checkDegree + " where updated_by='" + roomName + "' order by updated_at desc limit 1;"
    logger.info('sqlstring: %s', sqlstring)
    cur.execute(sqlstring)
    # rows = cur.fetchall()
    row = cur.fetchone()
    logger.info('row: %s', row)
    degree = row[0]

    # for index, item in enumerate(rows):
    print("roomName : ", roomName)
    print("checkDegree : ", checkDegree)
    print("degree : ", degree)
    print("Month : ", nowMonth)

    returnStr = ""
    if (int(nowMonth) >= 6 and int(nowMonth) <= 10):
        if (degree > 28):
            returnStr = {"status" : "hot", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}
        if (degree < 25):
            returnStr = {"status" : "cold", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}

    if (int(nowMonth) >= 11 and int(nowMonth) <= 5):
        if (degree > 22):
            returnStr = {"status" : "hot", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}
        if (degree < 18):
            returnStr = {"status" : "cold", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}

    cur.close()
    conn.close()
    logger.info('conn close.')

    return returnStr
    
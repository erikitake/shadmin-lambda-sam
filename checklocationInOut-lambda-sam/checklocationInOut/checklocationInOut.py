import logging
import json
import boto3
import urllib.parse
import os
import psycopg2
import requests
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

    locationAtAll = os.getenv('locationAtAll')
    locationAtAll = locationAtAll.split(":")
    print("locationAtAll : ", locationAtAll)

    # locationテーブルを更新している対象を取得し、その分処理を繰り返し
    sqlstring = "select updated_by from locations group by updated_by;"
    logger.info('sqlstring: %s', sqlstring)
    cur.execute(sqlstring)
    rows = cur.fetchall()
    logger.info('rows: %s', rows)

    # 更新している対象＞指定する場所でループして、直近2rowsでinoutに違いがあれば通知
    execNotification = {}
    n = 0
    for i, item in enumerate(rows):
        for j, locationAt in enumerate(locationAtAll):
            print("start : ", str(item), "locale : ", str(locationAt))
            arreyStr = execProcess(locationAt, item[0])
            if len(arreyStr)!=0 :
                execNotification["key"+str(n)] = arreyStr
                n = n + 1

    # Close communication with the database
    cur.close()
    conn.close()
    logger.info('conn close.')

    return execNotification


def execProcess(locationAt, item):
    db_connect = os.getenv('db_connect')
    conn = psycopg2.connect(db_connect)
    cur = conn.cursor()

    sqlstring = "select * from location_status where location_at = '" + str(locationAt) + "' and updated_by = '" + str(item) + "' order by updated_at desc limit 2;"
    logger.info('sqlstring: %s', sqlstring)
    cur.execute(sqlstring)
    rows = cur.fetchall()
    logger.info('rows: %s', rows)
    
    execNotification = ""
    if rows[0][3] == rows[1][3]:
        if rows[0][2] == rows[1][2]:
            print("no change")
        if rows[0][2] != rows[1][2]:
            print(rows[1][2] + " -> " + rows[0][2])
            if(rows[1][2] == 'in' and rows[0][2] == 'out' and locationAt == 'ikebukuro'):
                execNotification = {"locationAt": locationAt, "user": item, "mainStr": 'は帰ってます！！！', "flg": 0}
            if(rows[1][2] == 'out' and rows[0][2] == 'in' and locationAt == 'ikebukuro'):
                execNotification = {"locationAt": locationAt, "user": item, "mainStr": 'reached at office', "flg": 0} 
            if(rows[1][2] == 'in' and rows[0][2] == 'out' and locationAt == 'home'):
                execNotification = {"locationAt": locationAt, "user": item, "mainStr": 'went out at home', "flg": 0}
            if(rows[1][2] == 'out' and rows[0][2] == 'in' and locationAt == 'home'):
                execNotification = {"locationAt": locationAt, "user": item, "mainStr": 'reached at home', "flg": 0} 

    print("execNotification: ", execNotification)
    
    cur.close()
    conn.close()

    return execNotification
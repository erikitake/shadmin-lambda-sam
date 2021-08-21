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

    users = os.getenv('users')
    users = users.split(":")
    print("users : ", users)
    userStr = ""
    for index, user in enumerate(users):
        # 家にいるときのみ実行
        sqlstring = "select location_status from location_status where updated_by = '"+ user +"' and location_at = 'home' order by updated_at desc limit 1;"
        logger.info('sqlstring: %s', sqlstring)
        cur.execute(sqlstring)   # rows = cur.fetchall()
        row = cur.fetchone()
        logger.info('row: %s', row)
        if row[0] == 'out':
            print("外出中")
            return
        else:
            print(user, "さんは家にいる")

    # 部屋の気温をDBから取得
    sqlstring = "select degree from " + checkDegree + " where updated_by='" + roomName + "' order by updated_at desc limit 1;"
    logger.info('sqlstring: %s', sqlstring)
    cur.execute(sqlstring)   # rows = cur.fetchall()
    row = cur.fetchone()
    logger.info('row: %s', row)
    degree = row[0]

    # for index, item in enumerate(rows):
    print("roomName : ", roomName)
    print("checkDegree : ", checkDegree)
    print("degree : ", degree)
    print("Month : ", nowMonth)

    # 夏と冬で場合分け、快適な温度以外だったらjsonを作成
    returnStr = {"season" : "", "status" : "", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}
    if (int(nowMonth) >= 6 and int(nowMonth) <= 10):
        if (degree > 28):
            returnStr = {"season" : "summer", "status" : "hot", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}
            print("暑い")
        elif (degree < 25):
            returnStr = {"season" : "summer", "status" : "cold", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}
            print("寒い")
        else:
            print("快適")

    if (int(nowMonth) >= 11 and int(nowMonth) <= 5):
        if (degree > 22):
            returnStr = {"season" : "winter", "status" : "hot", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}
            print("暑い")
        elif (degree < 18):
            returnStr = {"season" : "winter", "status" : "cold", "roomName" : roomName, "checkDegree" : checkDegree, "degree" : degree}
            print("寒い")
        else:
            print("快適")

    cur.close()
    conn.close()
    logger.info('conn close.')

    return returnStr
    
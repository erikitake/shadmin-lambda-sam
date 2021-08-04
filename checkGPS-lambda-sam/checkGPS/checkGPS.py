from pyicloud import PyiCloudService
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

    APPLE_ID = os.getenv('APPLE_ID')
    PASSWORD = os.getenv('PASSWORD')
    COOKIE_DIR = '/tmp'
    COOKIE_FILE = os.getenv('COOKIE_FILE')
    COOKIE_SESSION = os.getenv('COOKIE_SESSION')
    PHONE_NAME = os.getenv('PHONE_NAME')
    # PHONE_NAME = "Aya"

    #cookieファイルをコピー
    shutil.copy2(COOKIE_FILE, COOKIE_DIR + '/' + COOKIE_FILE)
    shutil.copy2(COOKIE_SESSION, COOKIE_DIR + '/' + COOKIE_SESSION)

    #以下は接続するiCloudのアカウントとパスワードを記載します。
    api = PyiCloudService(apple_id=APPLE_ID, password=PASSWORD, cookie_directory=COOKIE_DIR)

    devices = api.devices
    print('devices: ', devices)
    itemIndex = 0
    for key in devices:
        # print(key)
        if (PHONE_NAME in str(key)):
            break    
        itemIndex = itemIndex + 1

    auth = api.devices[itemIndex].location()
    print("auth: ", auth)

#    nowtimestamp = datetime.datetime.fromtimestamp(int(auth['timeStamp']) / 1000)
    uTime = str(auth['timeStamp'])
    uTime = uTime[0:10]
    nowtimestamp = datetime.datetime.fromtimestamp(int(uTime))
    print("unix now: ", auth['timeStamp'])
    print("now: ", nowtimestamp)

    strGps = {"nowtimestamp": str(nowtimestamp), "latitude": auth['latitude'], "longitude": auth['longitude'], "horizontalAccuracy": auth['horizontalAccuracy'], "floorLevel": auth['floorLevel'], "altitude": auth['altitude'], "PHONE_NAME": PHONE_NAME}
    logger.info('str content %s', strGps)

    return strGps
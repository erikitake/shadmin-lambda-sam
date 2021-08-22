import json
import logging
import psycopg2
import os
import shutil
from datetime import datetime, timedelta, timezone
import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client('ssm')

def lambda_handler(event, context):
    logger.info('Event: %s', event)

    if event.get('season',None) == "":
        print('none')
        return {}
    
    season = event['season']
    status = event['status']
    roomName = event['roomName']
    checkDegree = event['checkDegree']
    degree = event['degree']

    nr_auth = ssm.get_parameter(Name='nr_auth', WithDecryption=True)['Parameter']['Value']
    print('nr_auth: ', nr_auth)
    nr_ac = ssm.get_parameter(Name='nr_ac', WithDecryption=True)['Parameter']['Value']
    url = "https://api.nature.global/1/appliances/" + nr_ac + "/aircon_settings"
    print('url: ', url)

    opmode = ""
    avol = ""
    adjustDegree = ""
    if season == "summer":
        opmode = "cool"
        if status == "hot":
            avol = "5"
            adjustDegree = "18"
        elif status == "cold":
            avol = "auto"
            adjustDegree = "26"
    elif season == "winter":
        opmode = "hot"
        if status == "cold":
            avol = "5"
            adjustDegree = "28"
        elif status == "hot":
            avol = "auto"
            adjustDegree = "22"

    param = "operation_mode="+opmode+"&air_volume="+avol+"&temperature="+adjustDegree
    print("param :", param)

    headers = {"accept":"application/json", "Content-Type":"application/x-www-form-urlencoded", "Authorization":nr_auth}
    r = requests.post(url, headers=headers, params=param)

    print("r status:", r.status_code)
    print("r :", r.json())

    # notify private line
    honbunStr = roomName + "の今の部屋の温度が" + str(degree) + "度だから、" + str(opmode) + " " + str(avol) + " " + str(adjustDegree) + "度 にエアコンを設定しました"
    mainStr = {"key0": {"flg": 0, "mainStr": honbunStr}}

    return mainStr
    
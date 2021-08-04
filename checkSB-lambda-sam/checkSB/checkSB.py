import logging
import requests
import json
import boto3
from datetime import datetime, timedelta, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client('ssm')

def lambda_handler(event, context):

    logger.info('Event: %s', context)

    url = ssm.get_parameter(Name='sb_url_meter', WithDecryption=True)['Parameter']['Value']
    logger.info('url: %s', url)
    sb_auth = ssm.get_parameter(Name='sb_auth', WithDecryption=True)['Parameter']['Value']
    logger.info('sb_auth: %s', sb_auth)
    
    headers = {"accept":"application/json", "Authorization":sb_auth}
    r = requests.get(url, headers=headers).json()

    dt_now = datetime.now()
    identiName = 'sb'
    tedegree = r['body']['temperature']
    tedatetime = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    hudegree = r['body']['humidity']
    hudatetime = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    ildegree = ''
    ildatetime = ''

    str = {"identiName": identiName, "tedegree": tedegree, "tedatetime": tedatetime, "hudegree": hudegree, "hudatetime": hudatetime, "ildegree": ildegree, "ildatetime": ildatetime}
    logger.info('str content %s', str)

    return str
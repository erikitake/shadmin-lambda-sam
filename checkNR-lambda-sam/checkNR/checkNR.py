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

    url = ssm.get_parameter(Name='nr_url', WithDecryption=True)['Parameter']['Value']
    logger.info('url: %s', url)
    nr_auth = ssm.get_parameter(Name='nr_auth', WithDecryption=True)['Parameter']['Value']
    logger.info('nr_auth: %s', nr_auth)
    
    headers = {"accept":"application/json", "Authorization":nr_auth}
    r = requests.get(url, headers=headers).json()

    identiName = 'nr'
    tedegree = r[0]['newest_events']['te']['val']
    tedatetime = r[0]['newest_events']['te']['created_at']
    hudegree = r[0]['newest_events']['hu']['val']
    hudatetime = r[0]['newest_events']['hu']['created_at']
    ildegree = r[0]['newest_events']['il']['val']
    ildatetime = r[0]['newest_events']['il']['created_at']

    str = {"identiName": identiName, "tedegree": tedegree, \
      "tedatetime": tedatetime, "hudegree": hudegree, \
      "hudatetime": hudatetime, "ildegree": ildegree, \
      "ildatetime": ildatetime}

    logger.info('str content %s', str)

    return str

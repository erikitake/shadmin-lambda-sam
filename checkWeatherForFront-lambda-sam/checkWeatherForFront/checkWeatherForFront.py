# coding: UTF-8

import logging
import requests
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info('Event: %s', context)

    APIKEY = os.getenv('APIKEY')
    BASEURL = os.getenv('BASEURL')
    PARAM = os.getenv('PARAM')

    url = BASEURL + PARAM + APIKEY
    r = requests.get(url).json()

    return r
    
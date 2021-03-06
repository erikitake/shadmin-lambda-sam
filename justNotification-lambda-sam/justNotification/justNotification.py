import logging
import requests
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

  logger.info('Event: %s', event)  
  for a in event:
    print(a, ": ", event[a])
    for b in event[a]:
      print(b, ": ", event[a][b])
    locationAt= ""
    if ('locationAt' in event[a]):
      locationAt = event[a]['locationAt']
    user = ""
    if ('user' in event[a]):
      user = event[a]['user']
    msg = ""
    if ('msg' in event[a]):
      msg = event[a]['msg']
    flg = "" 
    if ('flg' in event[a]):
      flg = event[a]['flg']

    # ライン通知(flgが0ならプライベート通知、それ以外ならメインの通知先)
    if int(flg) == 0:
        line_notify_token = os.getenv('lineTokenPriv')
    else:
        line_notify_token = os.getenv('lineTokenMain')
    if user != "" :
      msg = user + " " + msg 
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {msg}'}
    requests.post(line_notify_api, headers = headers, data = data)
    print("LINEに送信しました")

  return

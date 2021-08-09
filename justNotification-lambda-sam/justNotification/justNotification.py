import logging
import requests
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

  logger.info('Event: %s', event)  
  for a in event:
    # print(a, ": ", event[a])
    # for b in event[a]:
    #   print(b, ": ", event[a][b])
    locationAt = event[a]['locationAt']
    user = event[a]['user']
    msgStr = event[a]['mainStr']
    flag = event[a]['flg']

    # ライン通知(flagが0ならプライベート通知、それ以外ならメインの通知先)
    if flag == 0:
        line_notify_token = os.getenv('lineTokenPriv')
    else:
        line_notify_token = os.getenv('lineTokenMain')
    msgStr = user + " " + msgStr 
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {msgStr}'}
    requests.post(line_notify_api, headers = headers, data = data)
    print("LINEに送信しました")

  return

import logging
import string, random
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info('Event: %s', context)

#        '!', '"', '#', '$', '%', '&', "'", '(', ')', '=', '~',
#        '|', '-', '^', '@', '`', '+', '*', '<', '>', '_'
#使用できない記号が含まれる場合があるので制限
#        '$', '-', '.', ':', '@', '[', ']','_','#','&','?'

    symbols = '$-.:@[]_#&?'

    length = 2
    firstchar = random.choice(string.ascii_letters + string.digits)     # 先頭は大小英数字のみ
    allchars = ''

    for i in range(length):                                             # 大小英字は合計5、数字は3
        allchars = random.choice(string.ascii_letters) + allchars
        allchars = random.choice(string.ascii_letters) + allchars
        allchars = random.choice(string.digits) + allchars
    
    allchars = random.choice(string.digits) + allchars
    allchars = random.choice(symbols) + allchars                        # 記号は1文字のみ

    allchars = [firstchar] + random.sample(allchars, k=len(allchars))   # 2～8文字目は上記の文字列をランダムに並べ替え

    logger.info('allchars: %s', ''.join(allchars))

    return {
        'statusCode': 200,
        'body': json.dumps({"message": ''.join(allchars)})
    }
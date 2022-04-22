import time
import ast
import boto3
import json
from botocore.exceptions import UnknownKeyError
import logging
import secrets

AWS_REGION = 'us-east-1'

# logger settings
logger = logging.getLogger()
table_name = 'hm-serverless-analytics'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

sqs_client = boto3.client('sqs', region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)


def hm_analytics(event, context):
    print("STARTING PROCESSING MESSAGE")
    queue_url = 'https://sqs.us-east-1.amazonaws.com/825076716717/hm-analytics'

    try:

        message = json.loads(event["Records"][0]["body"])
        body = json.loads(message["body"])
        print(body)
        propertie_dto = body.get("propertieDto")

        analystic = {
            'id': str(message['id']),
            'neighborhood': propertie_dto['neighborhood'],
            'region': propertie_dto['region'],
            'size': int(propertie_dto['size']),
            'price': int(body['price'])
        }

        print('STARTING PUTTING INTO DYNAMODB -> ')
        response_dynamodb = table.put_item(TableName=table_name, Item=analystic)

        print("RESPONSE DYNAMODB -> {}".format(response_dynamodb))


    except Exception as err:
        print('ERROR OCCURRED -> {}'.format(err))
    else:
        print('Processed message | saved into dynamodb: {}'.format(response_dynamodb))

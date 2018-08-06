import os
from datetime import datetime
from urllib.request import Request, urlopen
import boto3

SITE = os.environ['site']  # URL of the site to check, stored in the site environment variable
EXPECTED = os.environ['expected']  # String expected to be on the page, stored in the expected environment variable


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = 'fieldcampaigner-data'
    prefix = 'campaign/'

    objects = []
    try:
        for obj in s3.list_objects(
            Bucket=bucket,
            Prefix=prefix)['Contents']:
            if obj['Key'] != prefix:
                objects.append(obj['Key'].replace(prefix, ''))
    except KeyError:
        objects = []
    print(objects)
        
        
# def lambda_handler_prout(event, context):
#     print('Checking {} at {}...'.format(SITE, event['time']))
#     try:
#         req = Request(SITE, headers={'User-Agent': 'AWS Lambda'})
#         if not validate(str(urlopen(req).read())):
#             raise Exception('Validation failed')
#     except:
#         print('Check failed!')
#         raise
#     else:
#         print('Check passed!')
#         return event['time']
#     finally:
#         print('Check complete at {}'.format(str(datetime.now())))

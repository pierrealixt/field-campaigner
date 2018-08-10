import boto3
import json

LAMBDA = [
    'features', 
    'osm_changesets', 
    'osm_features'
]

def invoke(function_name, payload):
    aws_lambda = boto3.client('lambda')
    aws_lambda.invoke(
        FunctionName='download_{}'.format(function_name),
        InvocationType='Event',
        Payload=payload)

def lambda_handler(event, context):
    uuid = event['campaign_uuid']
    payload = json.dumps({'campaign_uuid': uuid})

    for function_name in LAMBDA:
        invoke(function_name, payload)

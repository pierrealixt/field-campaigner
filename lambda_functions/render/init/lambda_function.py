import boto3
import json

LAMBDA = [
    'prout'
]

def invoke(function_name, payload):
    aws_lambda = boto3.client('lambda')
    aws_lambda.invoke(
        FunctionName='render_{}'.format(function_name),
        InvocationType='Event',
        Payload=payload)

def lambda_handler(event, context):
    uuid = event['campaign_uuid']
    payload = json.dumps({'campaign_uuid': uuid})

    for function_name in LAMBDA:
        invoke(function_name, payload)

def main():
    event = {'campaign_uuid': 'cabbf57b1ac3410cafdd6d64abb1c893'}
    lambda_handler(event, {})

if __name__ == "__main__":
    main()
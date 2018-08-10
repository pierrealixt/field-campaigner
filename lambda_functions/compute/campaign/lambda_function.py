import boto3
import json

def invoke(function_name, payload):
    aws_lambda = boto3.client('lambda')
    aws_lambda.invoke(
        FunctionName='init_{}'.format(function_name),
        InvocationType='RequestResponse',
        Payload=payload)


def lambda_handler(event, context):
    uuid = event['campaign_uuid']
    payload = json.dumps({'campaign_uuid': uuid})
    
    for action in ['download', 'process', 'render']:
        invoke(action, payload)

def main():
    event = {'campaign_uuid': 'cabbf57b1ac3410cafdd6d64abb1c893'}
    lambda_handler(event, {})

if __name__ == "__main__":
    main()
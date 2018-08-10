import boto3
import json
from aws import S3Data

def invoke(function_name, payload):
    aws_lambda = boto3.client('lambda')
    print('invoke', function_name)
    print(payload)
    # aws_lambda.invoke(
    #     FunctionName='process_{}'.format(function_name),
    #     InvocationType='Event',
    #     Payload=json.dumps(payload))

def lambda_handler(event, context):
    payload = {
        'campaign_uuid': event['campaign_uuid']
    }

    for function_name in ['feature_attribute_completeness','count_feature']:
        for filename in S3Data().list('data/overpass'):
            payload['overpass_filename'] = filename
            invoke(function_name, payload)

    for filename in S3Data().list('data/attic'):
        payload['attic_filename'] = filename
        invoke('mapper_engagement', payload)

    # osm_changesets
    # osm_features

def main():
    event = {'campaign_uuid': 'cabbf57b1ac3410cafdd6d64abb1c893'}
    lambda_handler(event, {})

if __name__ == "__main__":
    main()
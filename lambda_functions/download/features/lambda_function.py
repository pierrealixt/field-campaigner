import os
import json
import boto3
from aws import S3Data
from models.campaign import Campaign
from utilities import (
    get_unique_features,
    split_feature_key_values
)

def download_overpass_data(uuid, key, values):
    aws_lambda = boto3.client('lambda')

    payload = json.dumps({
        'campaign_uuid': uuid,
        'feature': {
            'key': key,
            'values': values
        }
    })
    aws_lambda.invoke(
        FunctionName='download_overpass_data',
        InvocationType='Event',
        Payload=payload)


def lambda_handler(event, context):
    uuid = event['campaign_uuid']
    
    campaign = Campaign(uuid)
    features = get_unique_features(
        functions=campaign._content_json['selected_functions'])
    
    for feature in features:
        key, values = split_feature_key_values(feature)
        download_overpass_data(uuid, key, values)


import os
from datetime import datetime
import boto3
import json
from campaign import Campaign

def compute_campaign(campaign_uuid):
    aws_lambda = boto3.client('lambda')
    payload = json.dumps({'campaign_uuid': campaign_uuid})
    aws_lambda.invoke(
        FunctionName='compute_campaign',
        InvocationType='Event',
        Payload=payload)

def lambda_handler(event, context):
    for campaign in Campaign.active():
        compute_campaign(campaign)

def main():
    lambda_handler({}, {})
    
if __name__ == "__main__":
    main()
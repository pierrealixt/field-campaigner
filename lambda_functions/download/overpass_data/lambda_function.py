import os
import hashlib
import requests
import boto3
import json
from aws import S3Data
from models.campaign import Campaign
from utilities import (
    split_polygon,
    feature_to_filename
)


# this function has a shitty name
# this function does two things: a POST request and create a file in S3
def get_data(filename, query):
    data = requests.post(
        url='http://exports-prod.hotosm.org:6080/api/interpreter',
        data={'data': query},
        headers={'User-Agent': 'HotOSM'})

    S3Data().create('data/overpass/{}.json'.format(filename), data.text.encode('utf-8'))

# find a way to remove template_query and template_query_with_value
def build_query(
    polygon=None,
    feature_key=None,
    feature_values=None
    ):
    
    template_query = (
        '('
        'way["%(KEY)s"]'
        '(poly:"{polygon}");'
        'node["%(KEY)s"]'
        '(poly:"{polygon}");'
        'relation["%(KEY)s"]'
        '(poly:"{polygon}");'
        ');'
        '(._;>;);'
        'out {print_mode};'
    )
    template_query_with_value = (
        '('
        'way["%(KEY)s"~"%(VALUE)s"]'
        '(poly:"{polygon}");'
        'node["%(KEY)s"~"%(VALUE)s"]'
        '(poly:"{polygon}");'
        'relation["%(KEY)s"~"%(VALUE)s"]'
        '(poly:"{polygon}");'
        ');'
        '(._;>;);'
        'out {print_mode};'
    )

    parameters = {
        'polygon': split_polygon(polygon),
        'print_mode': 'meta'
    }

    if feature_values:
        query = template_query_with_value % {
            'KEY': feature_key,
            'VALUE': '|'.join(feature_values)
        }
    else:
        query = template_query % {
            'KEY': feature_key
        }

    query = query.format(**parameters)

    query = '[out:json];' + query

    return query

def download_attic_data(uuid, feature, filename):
    aws_lambda = boto3.client('lambda')

    payload = json.dumps({
        'campaign_uuid': uuid,
        'filename': filename
    })
      # 'date': {
      #   'from': '2016-01-01',
      #   'to': '2018-08-31'
      # }

    print('download_attic_data')
    print(payload)
    # aws_lambda.invoke(
    #     FunctionName='download_attic_data',
    #     InvocationType='Event',
    #     Payload=payload)    


def lambda_handler(event, context):
    uuid = event['campaign_uuid']
    feature = event['feature']
    campaign = Campaign(uuid)
    query = build_query(
        polygon=campaign.corrected_coordinates(), 
        feature_key=feature['key'], 
        feature_values=feature['values'])

    filename = feature_to_filename(feature)
    # hashlib.md5(query.encode('utf-8')).hexdigest()
    get_data(filename, query)

    # not feature but date_start and date_end
    download_attic_data(uuid, feature, filename)
    

def main():
    event = {
        'campaign_uuid': 'cabbf57b1ac3410cafdd6d64abb1c893',
        'feature': {
            'key': 'amenity',
            'values': ['cafe']
        }
    }
    lambda_handler(event, {})

if __name__ == "__main__":
    main()
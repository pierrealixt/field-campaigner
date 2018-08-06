import os
import json
import boto3
from aws import S3Data


def download_overpass_file(uuid, feature):
    key = build_raw_data_overpass_path(
        campaign_path=campaign_path(uuid),
        feature=feature)

    S3Data().download_file(
        key=key,
        feature=feature,
        destination='/tmp')


def invoke_render_feature(uuid, feature):
    payload = json.dumps({
        'campaign_uuid': uuid,
        'feature': feature
    })

    aws_lambda = boto3.client('lambda')
    function_name_with_env = '{env}_{function_name}'.format(
        env=os.environ['ENV'],
        function_name='render_feature')

    aws_lambda.invoke(
        FunctionName=function_name_with_env,
        InvocationType='Event',
        Payload=payload)    


def save_data(uuid, type_id, data):
    with open('/tmp/data.json', 'w') as file:
        json.dump(data, file)

    data_path = build_data_path(
        campaign_path=campaign_path(uuid),
        type_id=type_id)

    with open('/tmp/data.json', 'rb') as data:
        S3Data().upload_file(
            key=data_path,
            body=data)


def compute_completeness_pct(features_collected, features_completed):
    completeness_pct = '0.0'
    if features_collected > 0:
        completeness_pct = '%.1f' % (
        (features_completed / features_collected) * 100)
    return completeness_pct



def campaign_path(uuid):
    return '/'.join([
        'campaigns',
        '{uuid}']).format(
            uuid=uuid)


def build_render_data_path(campaign_path, type_id):
    return '/'.join([
        '{campaign_path}',
        'render/{type_id}']).format(
            campaign_path=campaign_path,
            type_id=type_id)


def build_data_path(campaign_path, type_id):
    return '/'.join([
        '{render_data_path}',
        'feature_completeness.json']).format(
            render_data_path=build_render_data_path(
                campaign_path=campaign_path,
                type_id=type_id))


def fetch_campaign(campaign_path):
    return S3Data().fetch('{campaign_path}/campaign.json'.format(
        campaign_path=campaign_path))


def build_raw_data_overpass_path(campaign_path, feature):
    return '/'.join([
        '{campaign_path}',
        'raw_data/overpass',
        '{feature}.xml']).format(
            campaign_path=campaign_path,
            feature=feature)


def fetch_required_tags(seeked_feature, functions):
    return list(dict(filter(lambda function:
        is_function_and_feature(
            function_name=function[1]['function'],
            feature=function[1]['feature'],
            seeked_feature=seeked_feature),
        functions.items())).values())[0]['attributes']


def fetch_type(seeked_feature, functions):
    return list(dict(filter(lambda function:
        is_function_and_feature(
            function_name=function[1]['function'],
            feature=function[1]['feature'],
            seeked_feature=seeked_feature),
        functions.items())).values())[0]['type']


def is_function_and_feature(function_name, feature, seeked_feature):
    return \
        function_name == 'FeatureAttributeCompleteness' \
        and \
        feature == seeked_feature


def save_to_s3(path, data):    
    S3Data().create(
        key=path,
        body=json.dumps(data))
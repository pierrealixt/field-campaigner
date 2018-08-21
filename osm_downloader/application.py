import logging
import json
import flask
from flask import request, Response
import boto3
from campaign import Campaign
from utilities import (
    date_to_dict,
    build_overpass_query,
    build_attic_query,
    build_diff_attic_query,
    save_to_s3,
    build_overpass_path,
    build_attic_path,
    post_request,
    build_payload,
    invoke_download_attic_data
)


application = flask.Flask(__name__)
application.config.from_object('default_config')
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

@application.route('/download-feature', methods=['POST'])
def download_feature():
    print('Receiving message...')
    import datetime
    print(datetime.datetime.now())

    data = json.loads(request.data)
    uuid = data['campaign_uuid']
    print('campaign uuid:', uuid)
    feature = data['feature']
    print('feature:', feature)
    campaign = Campaign(uuid)

    # overpass
    print('downloading overpass...')
    print(datetime.datetime.now())
    query = build_overpass_query(
        polygon=campaign.corrected_coordinates(),
        feature=feature)
    print(datetime.datetime.now())

    save_to_s3(
        path=build_overpass_path(uuid, feature),
        data=post_request(query))
    print('done.')
    print(datetime.datetime.now())
    print('downloading attic...')
    # attic
    date = {
        'from': campaign.start_date,
        'to': campaign.end_date
    }

    query = '{diff_query}{query}'.format(
        diff_query=build_diff_attic_query(date),
        query=build_attic_query(uuid, feature))
    print(datetime.datetime.now())
    save_to_s3(
        path=build_attic_path(uuid, feature),
        data=post_request(query))
    print(datetime.datetime.now())   
    print('done.')
    return Response("", status=200)


if __name__ == '__main__':
    application.run(host='0.0.0.0')
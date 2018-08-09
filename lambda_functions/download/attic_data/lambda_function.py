import hashlib
import requests
import datetime
from models.campaign import Campaign
from aws import S3Data
from utilities import (
    cast_date_to_timgm,
    cast_element_ids_to_s,
    serialize_overpass_data,
    format_query
)

# this function has a shitty name
# this function does two things: a POST request and create a file in S3
def get_data(filename, query):
    data = requests.post(
        url='http://overpass-api.de/api/interpreter',
        data={'data': query},
        headers={'User-Agent': 'HotOSM'})
    S3Data().create('data/attic/{}.xml'.format(filename), data.text.encode('utf-8'))


def build_diff_query(date):
    date_from = cast_date_to_timgm(date['from'])
    date_to = cast_date_to_timgm(date['to'])

    datetime_from = datetime.datetime.utcfromtimestamp(
            float(date_from) / 1000.)
    datetime_to = datetime.datetime.utcfromtimestamp(
            float(date_to) / 1000.)
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    diff_query = '[diff:"{date_from}", "{date_to}"];'.format(
            date_from=datetime_from.strftime(date_format),
            date_to=datetime_to.strftime(date_format)
    )
    return diff_query

def build_query(filename):
    elements_ids = serialize_overpass_data(filename)

    parameters = {
        'element_parameters': cast_element_ids_to_s(elements_ids),
        'print_mode': 'meta'
    }
    return format_query(parameters)

def lambda_handler(event, context):
    diff_query = build_diff_query(event['date'])
    query = build_query(event['overpass_filename'])
    query = diff_query + query

    filename = hashlib.md5(query.encode('utf-8')).hexdigest()
    get_data(filename, query)


def main():
    event = {
      'campaign_uuid': 'cabbf57b1ac3410cafdd6d64abb1c893',
      'overpass_filename': '8e7de04ca4dc16b634b56a0824b6359d',
      'date': {
        'from': '2016-01-01',
        'to': '2018-08-31'
      }
    }
    lambda_handler(event, {})

if __name__ == "__main__":
    main()
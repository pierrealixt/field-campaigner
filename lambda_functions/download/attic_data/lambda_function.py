from utilities import (
    build_diff_query,
    build_query,
    post_request,
    save_to_s3
)

def lambda_handler(event, context):
    diff_query = build_diff_query(event['date'])
    query = build_query(event['filename'])
    query = diff_query + query

    save_to_s3(
        filename=event['filename'],
        data=post_request(query))


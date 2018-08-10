
from models.campaign import Campaign
from utilities import (
    feature_to_filename,
    date_to_dict,
    build_query,
    save_to_s3,
    post_request,
    download_attic_data,
    build_payload
)


def lambda_handler(event, context):
    uuid = event['campaign_uuid']
    
    feature = event['feature']
    filename = feature_to_filename(feature)

    campaign = Campaign(uuid)
    date = date_to_dict(campaign.start_date, campaign.end_date)

    query = build_query(
        polygon=campaign.corrected_coordinates(), 
        feature=feature)

    save_to_s3(
        filename=filename, 
        data=post_request(query))

    download_attic_data(
        payload=build_payload(uuid, filename, date))
    


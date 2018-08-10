from models.campaign import Campaign
from utilities import (
    serialize_geometry,
    save_to_s3,
    get_request
)

def lambda_handler(event, context):
    uuid = event['campaign_uuid']
    campaign = Campaign(uuid)
    geometry = serialize_geometry(campaign.geometry)
    start_date = campaign.start_date
    end_date = campaign.end_date

    save_to_s3(
        filename=uuid,
        data=get_request(geometry, start_date, end_date))
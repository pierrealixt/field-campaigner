from aws import S3Data

def fetch_attributes(feature, functions):
    function = 'FeatureAttributeCompleteness'
    for function_id in functions:
        if functions[function_id]['function'] == function:
            if functions[function_id]['feature'] == feature: 
                return functions[function_id]['attributes']

def lambda_handler(event, context):
    feature = event['overpass_filename'].replace('.json', '')
    campaign = S3Data().fetch('campaign/{}.json'.format(event['campaign_uuid']))
    attributes = fetch_attributes(feature, campaign['selected_functions'])

    osm_data = S3Data().fetch('data/overpass/{}'.format(event['overpass_filename']))    
    features = osm_data['elements']

    print(attributes)

def main():
    event = {
      'campaign_uuid': 'cabbf57b1ac3410cafdd6d64abb1c893',
      'overpass_filename': 'amenity=cafe.json'
    }
    lambda_handler(event, {})

if __name__ == "__main__":
    main()
import qrcode
import requests
import json

import os

def create_geo_coordinate_qr(latitude, longitude):
    # returns pillow image
    location = f'geo:{latitude},{longitude}'

    return qrcode.make(location)

def create_address_qr(address):
    # returns pillow image
    coordinates = get_geolocation(address)

    if coordinates is not None:
        return create_geo_coordinate_qr(latitude=coordinates.get('latitude'), longitude=coordinates.get('longitude'))
    return None

def get_geolocation(address):

    response = make_request(address=address)
    
    # check if response exist
    if response is not None:
        if len(response.get('results')) == 0:
            return None

        coordinate = {}

        coordinate['address'] = address
        coordinate['latitude'] = response['results'][0]['geometry']['location']['lat']
        coordinate['longitude'] = response['results'][0]['geometry']['location']['lng']

        return coordinate
    
    return None


def get_address(latitude, longitude):
    # retuns address string
    response = make_request(geocoding_type='reverse_geocoding', latitude=latitude, longitude=longitude)

    if response is not None:

        if len(response.get('results')) == 0:
            return None
        
        address = response['results'][0]['formatted_address']

        return address

    return None

def make_request(geocoding_type='geocoding', address='', latitude='', longitude=''):
    if geocoding_type in ['geocoding', 'reversse_geocoding']:
        # returns dictionary of coordinates
        with open(os.path.join(os.getcwd(), 'qrcodes', 'config', 'config.json')) as config_file:
            coordinate = {}

            config = json.load(config_file)

            google_api_config = config.get('google').get('maps').get('api')
            geocoding_config = google_api_config.get(geocoding_type)

            api_key = google_api_config.get('key')
            geocoding_url = geocoding_config.get('url')

            url = geocoding_url.format(**locals())

            response = requests.get(url)

            json_response = json.loads(response.text)

            return json_response
    return None    
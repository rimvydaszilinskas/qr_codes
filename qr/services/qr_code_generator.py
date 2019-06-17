import wifi_qrcode_generator
import qrcode
import json

# constants - possible values for wifi security
WPA_AUTHENTICATION = 'WPA'
WEP_AUTHENTICATION = 'WEP'
NO_AUTHENTICATION = 'nopass'

def generate_wifi_qrcode(ssid, password=None, authentication_type=None, hidden=False):
    # setup the data correctly
    if authentication_type is None or authentication_type == 'nopass':
        authentication_type = 'nopass'
        password = None

    # return generated qr code as PIL object 
    return wifi_qrcode_generator.wifi_qrcode(ssid, hidden, authentication_type, password)

def generate_link_qrcode(link='https://rimvydas.site'):
    # the link should start with http:// or https://
    if not link.startswith('http://') or not link.startswith('https://'):
        link = 'http://' + link
    
    # return link qr code as PIL object
    return qrcode.make(data=link)

def load_wifi_data_from_json(wifi_string):
    wifi_config = json.loads(wifi_string)

    # change the password field correctly
    wifi_config['password'] = None if wifi_config['security'] == 'nopass' else wifi_config['password']

    return wifi_config
from django.test import TestCase
from qrcodes.services.location_qr_generator import create_geo_coordinate_qr, get_geolocation
from qrcodes.services.vcard_generator import get_phone_type

class LocationTestCase(TestCase):
    def test_get_coordinate(self):
        coordinate = create_geo_coordinate_qr(1, 2)

        self.assertNotEqual(coordinate, None)
    
    def test_get_address_coordinate(self):
        coordinate = get_geolocation('sandasjndasjnadsasndj cjka sjk asj d')

        self.assertEqual(coordinate, None)

class VCardTestCase(TestCase):
    def test_phone_type(self):
        phone_type = get_phone_type('TYPE=HOME:+111111')

        self.assertEqual(phone_type, 'HOME')

    def test_phone_type_none(self):
        phone_type = get_phone_type('PHONEs=PHONEsss:444')
        print(f'-------------------------------------{phone_type}')
        self.assertEqual(phone_type, None)
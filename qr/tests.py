from django.test import TestCase

from qr.services.location_qr_generator import create_geo_coordinate_qr, get_geolocation
from qr.services.vcard_generator import VCardGenerator

class LocationTestCase(TestCase):
    def test_get_coordinate(self):
        coordinate = create_geo_coordinate_qr(1, 2)

        self.assertIsNotNone(coordinate)

    def test_get_address(self):
        coordinate = get_geolocation('Lygten 37, Copenhagen')

        self.assertIsNotNone(coordinate)

class VCardTestCase(TestCase):
    def test_create_instance(self):
        vcard = VCardGenerator()

        self.assertIsNotNone(vcard)

    def test_vcard_loads(self):
        vcard = VCardGenerator()

        testString = 'BEGIN:VCARD\nVERSION:4.0\nN:Zilinskas;Rimvydas;;;\nORG:1997\nTEL;TYPE=HOME;VALUE=uri:tel:+4527280136\nEMAIL:rimvydas.zilinskas@yahoo.com\nEND:VCARD'

        vcard.loads(testString)

        self.assertDictEqual(vcard.get_as_dictionary(), {'firstname': 'Rimvydas', 'lastname': 'Zilinskas', 'phones': [{'number': '+4527280136', 'type': 'HOME'}], 'email': 'rimvydas.zilinskas@yahoo.com', 'organization': '1997', 'title': None})

    def test_vcard_sets(self):
        vcard = VCardGenerator()

        vcard.set_email('rimvydas.zilinskas@yahoo.com')
        vcard.set_firstname('Rimvydas')
        vcard.set_lastname('Zilinskas')
        vcard.set_organization('Ticketbutler')
        vcard.set_title('Junior Developer')
        vcard.add_phone(phone='+4527280136', phone_type='MOBILE')

        self.assertDictEqual(vcard.get_as_dictionary(), {'firstname': 'Rimvydas', 'lastname': 'Zilinskas', 'phones': [{'number': '+4527280136', 'type': 'MOBILE'}], 'email': 'rimvydas.zilinskas@yahoo.com', 'organization': 'Ticketbutler', 'title': 'Junior Developer'})

class TestLinkView(TestCase):
    def test_root_redirect(self):
        response = self.client.get('/')
    
        self.assertEqual(response.status_code, 302)

    def test_view_accessible(self):
        response = self.client.get('/link/')

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/link/', data={'link': 'google.com'})

        self.assertEqual(response.status_code, 200)
from django.shortcuts import render, redirect
from django.views import View
from django.http import FileResponse, HttpResponse
from io import BytesIO
import json
import re

from .services.qr_code_generator import generate_link_qrcode, generate_wifi_qrcode
from .services.vcard_generator import VCardGenerator
from .services.location_qr_generator import create_address_qr, create_geo_coordinate_qr

class Index(View):
    def get(self, request):
        return redirect('link/')

class Links(View):
    def get(self, request):
        return render(request, 'qr/link.html')

    def post(self, request):
        link_string = request.POST['link']

        qr = generate_link_qrcode(link=link_string)

        image_io = BytesIO()

        qr.save(image_io, format='PNG')

        image_io.seek(0)

        return FileResponse(image_io, as_attachment=True, filename='link_qr.png')

class Contacts(View):
    def get(self, request):
        context = {
            'phone_numbers': [1, 2, 3]
        }

        return render(request, 'qr/contact.html', context)

    def post(self, request):
        vcard = VCardGenerator()

        for key in request.POST:
            if key.startswith('phone'):
                if request.POST.get(key) != '':
                    identifier = re.findall(r'\d+', key)[0]
                    vcard.add_phone(phone=request.POST.get(key), phone_type=request.POST.get(f'type{identifier}').upper())

        vcard.set_firstname(request.POST.get('firstname', None))
        vcard.set_lastname(request.POST.get('lastname', None))
        vcard.set_organization(request.POST.get('organisation', None))
        vcard.set_title(request.POST.get('job_title', None))
        vcard.set_email(request.POST.get('email', None))

        file_type = request.POST.get('file')

        if file_type == 'qr':
            img = vcard.get_qr()

            image_io = BytesIO()
            img.save(image_io, format='PNG')
            img.seek(0)

            return FileResponse(image_io, as_attachment=True, filename='vcard.png')
        else:
            vcard_out = vcard.generate_string()

            response = HttpResponse(vcard_out, content_type='text/plain')

            response['Content-Disposition'] = f'attachment; filename=vcard.vcf'
            
            return response

class ContactUpload(View):
    def get(self, request):
        return render(request, 'qr/vcard_upload.html')

    def post(self, request):
        contact_str = request.FILES['file'].read().decode('UTF-8')

        contact = VCardGenerator()

        contact.loads(contact_str)

        context = {
            'contact': contact.get_as_dictionary(),
            'phone_numbers': range(len(contact.get_phones()), 3)
        }

        return render(request, 'qr/contact.html', context=context)

class Location(View):
    def get(self, request):
        return render(request, 'qr/location.html')

    def post(self, request):
        data = request.POST

        if data.get('file') == 'qr':
            if data.get('address') != '':
                filename = post_data.get('address')
                qr = create_address_qr(filename)
            else:
                filename = 'location'
                qr = create_geo_coordinate_qr(latitude=data.get('latitude'), longitude=data.get('longitude'))

            image_io = BytesIO()

            qr.save(image_io, format='PNG')
            image_io.seek(0)

            return FileResponse(image_io, as_attachment=True, filename=f'{filename}_qr.png')
        else:
            if post_data.get('address') != '':
                address = post_data.get('address')
                filename = post_data.get('address')
                coordinates = get_geolocation(post_data.get('address'))
            else:
                coordinates = {
                    'latitude': post_data.get('latitude'),
                    'longitude': post_data.get('longitude')
                }
                
                filename = 'location'

                # decode the coordinates to get the address
                address = get_address(coordinates['latitude'], coordinates['longitude'])
            
            # put dump everything to json string
            coordinates['address'] = address
            coordinates_str = json.dumps(coordinates)

            # set content type
            response = HttpResponse(coordinates_str, content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename={filename}_config.json'

            return response

class LocationUpload(View):
    def get(self, request):
        return render(request, 'qr/location_upload.html')
    def post(self, request):
        # decode json file and display it on
        location_file = request.FILES['file']

        location_str = location_file.read().decode('UTF-8')

        location_data = json.loads(location_str)

        context = {
            'location': location_data
        }

        return render(request, 'qrcodes/location.html', context=context)

class Wifi(View):
    def get(self, request):
        return render(request, 'qr/wifi.html')

    def post(self, request):
        post_data = request.POST

        ssid = post_data['ssid']
        password = post_data['password']
        authentication_type = post_data['security']
        hidden = post_data['hidden'] == 'hidden'

        file_type = post_data['file']

        # if required file is a qrcode
        if file_type == 'qr':
            qr = generate_wifi_qrcode(ssid=ssid,
                                        password=password,
                                        authentication_type=authentication_type,
                                        hidden=hidden)

            image_io = BytesIO()

            qr.save(image_io, format='PNG', quality=70)
            image_io.seek(0)

            return FileResponse(image_io, as_attachment=True, filename=f'{ssid}_config_qr.png')
        # if required file is json        
        else:
            wifi_config = {
                'ssid': ssid,
                'password': password,
                'authentication_type': authentication_type,
                'hidden': hidden
            }

            wifi_config_str = json.dumps(wifi_config)

            response = HttpResponse(wifi_config_str, content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename={ssid}_config.json'

            return response

class WifiUpload(View):
    def get(self, request):
        return render(request, 'qr/wifi_upload.html')

    def post(self, request):
        # decode json file and display it on the form
        wifi_file = request.FILES['file']

        wifi_str = wifi_file.read().decode('UTF-8')

        wifi_data = json.loads(wifi_str)

        context = {
            'wifi': wifi_data
        }

        return render(request, 'qrcodes/wifi.html', context=context)
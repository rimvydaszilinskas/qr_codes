from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse, FileResponse
from io import BytesIO
import re

import json

from .services.qr_code_generator import generate_link_qrcode, generate_wifi_qrcode
from .services.vcard_generator import generate_vcard_qrcode, generate_vcard_string, load_data_from_vcard
from .services.location_qr_generator import create_geo_coordinate_qr, create_address_qr, get_geolocation, get_address

# All the routes support GET and POST request. GET renders the view and POST handles form inputs

def index(request):
    # default path redirects to link qr generator
    return redirect('qrcodes:link')

def link(request):
    if request.method == 'GET':
        return render(request, 'qrcodes/link.html')
    elif request.method == 'POST':
        # Get the link
        link_string = request.POST['link']

        qr = generate_link_qrcode(link=link_string)

        # We will have to save image as bytes to stram it back
        image_io = BytesIO()

        qr.save(image_io, format='PNG', quality=70)
        image_io.seek(0)

        # stream image back as a FileResponse
        return FileResponse(image_io, as_attachment=True, filename='qr.png')
    else:
        return HttpResponseNotAllowed(request)

def contact(request):
    if request.method == 'GET':
        # array for displaying variable ammount of phone number fields
        context = {
            'phone_numbers': [1, 2, 3]
        }

        return render(request, 'qrcodes/contact.html', context)
    elif request.method == 'POST':
        # Get the form data
        post_data = request.POST

        # initialize empty phone list to fill it up later on
        phones = []

        # phones have to be an array
        for key in post_data:
            if key.startswith('phone'):
                if post_data.get(key) != '':
                    # extrude the number from the key, that is going to be identifier
                    identifier = re.findall(r'\d+', key)[0]
                    
                    # Add a phone to the list
                    phones.append({
                        'type': post_data.get(f'type{identifier}').upper(),
                        'number': post_data.get(key)
                        })

        # get the data from the form
        firstname = post_data.get('firstname')
        lastname = post_data.get('lastname')
        organisation = post_data.get('organisation')
        job_title = post_data.get('job_title')
        email = post_data.get('email')

        file_type = post_data.get('file')

        if file_type == 'qr':
            qr = generate_vcard_qrcode(firstname=firstname, lastname=lastname, organisation=organisation,
                                        job_title=job_title, phone=phones, email=email)

            image_io = BytesIO()
            
            # save image as byte stream
            qr.save(image_io, format='PNG', quality=70)
            image_io.seek(0)
            
            # send back a file named as firstname_lastname_qr.png
            return FileResponse(image_io, as_attachment=True, filename=f'{firstname}_{lastname}_qr.png')
        elif file_type == 'vcf':
            vcard = generate_vcard_string(firstname=firstname, lastname=lastname, organisation=organisation,
                                            job_title=job_title, phone=phones, email=email)

            # set content type for the browser to expect text based file
            response = HttpResponse(vcard, content_type='text/plain')

            # send back a file named as firstname_lastname.vcf
            response['Content-Disposition'] = f'attachment; filename={firstname}_{lastname}.vcf'

            return response
        # if neither of the options is present just render the contact form
        return render(request, 'qrcodes/contact.html')        
    else:
        return HttpResponseNotAllowed(request)


def contact_upload(request):
    # read the data from .vcf file and display on the form
    if request.method == 'GET':
        return render(request, 'qrcodes/vcard_upload.html')
    elif request.method == 'POST':
        # decode the file as UTF-8
        contact_str = request.FILES['file'].read().decode('UTF-8')

        contact_data = load_data_from_vcard(contact_str)

        context = {
            'contact': contact_data,
            'phone_numbers': range(len(contact_data['phone']), 3)
        }

        return render(request, 'qrcodes/contact.html', context=context)
    else:
        return HttpResponseNotAllowed(request)

def location(request):
    if request.method == 'GET':
        return render(request, 'qrcodes/location.html')
    elif request.method == 'POST':
        post_data = request.POST
        
        if post_data.get('file') == 'qr':
            # chick if address is present
            if post_data.get('address') != '':
                # create a qr based on address
                filename = post_data.get('address')
                qr = create_address_qr(post_data.get('address'))
            else:
                # address is not defined, create qr based on geoloction
                filename = 'location'
                qr = create_geo_coordinate_qr(latitude=post_data.get('latitude'), longitude=post_data.get('longitude'))

            image_io = BytesIO()

            qr.save(image_io, format='PNG', quality=70)
            image_io.seek(0)

            return FileResponse(image_io, as_attachment=True, filename=f'{filename}_qr.png')
        else:
            # check if address is present
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
    else:
        return HttpResponseNotAllowed(request)

def location_upload(request):
    if request.method == 'GET':
        return render(request, 'qrcodes/location_upload.html')
    elif request.method == 'POST':
        # decode json file and display it on
        location_file = request.FILES['file']

        location_str = location_file.read().decode('UTF-8')

        location_data = json.loads(location_str)

        context = {
            'location': location_data
        }

        return render(request, 'qrcodes/location.html', context=context)
    else:
        return HttpResponseNotAllowed(request)

def wifi(request):
    if request.method == 'GET':
        return render(request, 'qrcodes/wifi.html')
    elif request.method == 'POST':
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
    else:
        return HttpResponseNotAllowed(request)

def wifi_upload(request):
    if request.method == 'GET':
        return render(request, 'qrcodes/wifi_upload.html')
    elif request.method == 'POST':
        # decode json file and display it on the form
        wifi_file = request.FILES['file']

        wifi_str = wifi_file.read().decode('UTF-8')

        wifi_data = json.loads(wifi_str)

        context = {
            'wifi': wifi_data
        }

        return render(request, 'qrcodes/wifi.html', context=context)
    else:
        return HttpResponseNotAllowed(request)
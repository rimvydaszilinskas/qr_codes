from django.shortcuts import render

def link(request):
    context = {}

    return render(request, 'qrcodes/link.html', context)

def contact(request):
    context = {}

    return render(request, 'qrcodes/contact.html', context)

def contact_upload(request):
    context = {}

    return render(request, 'qrcodes/vcard_upload.html', context)

def location(request):
    context = {}

    return render(request, 'qrcodes/location.html', context)

def location_upload(request):
    context = {}

    return render(request, 'qrcodes/location_upload.html', context)

def wifi(request):
    context = {}

    return render(request, 'qrcodes/wifi.html', context)

def wifi_upload(request):
    context = {}

    return render(request, 'qrcodes/wifi_upload.html', context)
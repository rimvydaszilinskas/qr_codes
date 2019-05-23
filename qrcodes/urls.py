from django.urls import path

from . import views

app_name = 'qrcodes'

urlpatterns = [
    path('', views.index, name='index'),
    path('link/', views.link, name='link'),
    path('contact/', views.contact, name='contact'),
    path('contact/upload', views.contact_upload, name='contact_upload'),
    path('location', views.location, name='location'),
    path('location/upload', views.location_upload, name='location_upload'),
    path('wifi', views.wifi, name='wifi'),
    path('wifi/upload', views.wifi_upload, name='wifi_upload')
]
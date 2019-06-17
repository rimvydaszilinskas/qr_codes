from django.urls import path

from . import views

app_name = 'qr'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('link/', views.Links.as_view(), name='link'),
    path('contact/', views.Contacts.as_view(), name='contact'),
    path('contact/upload', views.ContactUpload.as_view(), name='contact_upload'),
    path('location', views.Location.as_view(), name='location'),
    path('location/upload', views.LocationUpload.as_view(), name='location_upload'),
    path('wifi', views.Wifi.as_view(), name='wifi'),
    path('wifi/upload', views.WifiUpload.as_view(), name='wifi_upload')
]
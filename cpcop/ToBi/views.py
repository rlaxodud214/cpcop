from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def traffic(request):
    lat = request.GET.get('latitude')
    long = request.GET.get('longitude')
    data = {'title': 'Traffic', 'lat': lat, 'long': long, 'loc':Reverse_location(lat,long)}
    return render(request, 'ToBi/traffic.html', data)

def weather(request):
    lat = request.GET.get('latitude')
    long = request.GET.get('longitude')
    data = {'title': 'Weather', 'lat': lat, 'long': long, 'loc':Reverse_location(lat,long)}
    return render(request, 'ToBi/weather.html', data)

def schedule(request):
    data = {'title': 'Schedule'}
    return render(request, 'ToBi/schedule.html', data)


################################################################
#여기부터는 다른 파일로 옮길예정
###############################################################
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, unquote
import urllib
import json

def Reverse_location(lat,lon):     #파라미터로 위도 경도 와야함(문자열 형으로)
    lat = lat  # 한국산업기술대학교 위도("37.340037")
    lon = lon  # 한국산업기술대학교 경도("126.733381")
    key = "l7xx00cd3e8e95cc4fee84f48861b2d6d812"  # api 키

    url = "https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1"
    queryParams = "&" + urlencode({quote_plus('lat'): lat,
                                   quote_plus('lon'): lon,
                                   quote_plus('coordType'): "WGS84GEO",
                                   quote_plus('addressType'): "A01",
                                   quote_plus('appKey'): key})

    request = urllib.request.Request(url + unquote(queryParams))
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    decode = response_body.decode('utf-8')
    json_data = json.loads(decode)
    return(json_data["addressInfo"]["fullAddress"])  # json을 조작하여 위도경도 다시 반환가능
		#주소정보 반환(문자형으로 반환)



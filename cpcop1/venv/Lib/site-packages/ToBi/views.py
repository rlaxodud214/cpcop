from django.shortcuts import render

# Create your views here.
import ToBi.transfer.Near_Bus_Station as Near_Bus_Station
import ToBi.transfer.Near_Sub_Station as Near_Sub_Station
import ToBi.transfer.eclass as eclass
import ToBi.transfer.Shuttle_Time_go as Shuttle_Time_go
import ToBi.transfer.Span_Time as Span_Time
import ToBi.transfer.Sub_Time as Sub_Time
import ToBi.transfer.dict_go as dict_go
import ToBi.transfer.location as location
import time

def login(request):
    return render(request, 'login.html')

def index(request):
    id = request.POST['username']
    pw = request.POST['password']
    return render(request, 'index.html',{'id':id, 'pw':pw})

def traffic(request):
    lat = request.POST['latitude']
    long = request.POST['longitude']
    id = request.POST['username']
    pw = request.POST['password']
    start = time.time()
    dictgo = dict_go.dict_time_table_go
    nearsub1 = Near_Sub_Station.Near_Sub_Station('37.492117', '127.031322')  # 좌표(현재 위치) -> 정왕역 (좌표로 부터 가까운 역 검색)
    index1 = nearsub1.rstrip('역')
    n = 1
    weeks = ['월', '화', '수', '목', '금']
    dataset = eclass.eclass(id,pw)[weeks[n]] #"2019152025", 'su9191su?k'
    h1 = int(dataset['hour'])
    m1 = int(dataset['minute'])
    std = Shuttle_Time_go.Shuttle_Time_go(h1, m1, dictgo)
    h2 = int(std[0])
    m2 = int(std[1])
    dict1 = {}
    dict1['starty'], dict1['startx'] = location.dict_location[index1]
    time_info = Span_Time.Span_Time(dict1['startx'], dict1['starty'])
    h3, m3 = Sub_Time.Sub_Time(h2, m2, int(time_info))
    Travel_time_bus = Near_Bus_Station.Near_Bus_Station('37.492117', '127.031322')
    h4, m4 = Sub_Time.Sub_Time(h3, m3, Travel_time_bus)
    h5, m5 = Sub_Time.Sub_Time(h4, m4, 10)
    intro = "출발 시스템" + "-" * 60
    near = "현재 " + str(Reverse_location('37.492117', '127.031322')) + "의 위치에서 가장 가까운 역은 " + str(index1) + "역입니다."
    recommend = "출발 추천시간 (집-> 버스정류장) : " + str(h5) + "시 " + str(m5) + "분(예상소요시간 : 10분)"
    bus = ''
    gogo = nearsub1 + "에서 출발해야하는 시간 : " + str(h3) + "시 " + str(m3) + "분(예상소요시간 : " + time_info + "분)"
    station = "정왕역에서 출발하는 " + str(h2) + "시 " + str(m2) + "분 셔틀 탑승"
    school = "학교에 도착해야하는 시간 : %d시 %d분 (시간표 정보 읽어오기)\n" % (h1, m1)
    rjfflstlrks = time.time() - start
    during = '응답시간 = ' + str(rjfflstlrks)
    data = {'title': 'Traffic', 'lat': lat, 'long': long, 'loc':Reverse_location(lat,long), 'intro':intro,
            'near':near, 'recommend':recommend, 'bus':bus, 'gogo':gogo, 'station':station, 'school':school, 'during':during, 'id':id, 'pw':pw}
    return render(request, 'ToBi/traffic.html', data)

def weather(request):
    lat = request.POST['latitude']
    long = request.POST['longitude']
    id = request.POST['username']
    pw = request.POST['password']
    data = {'title': 'Weather', 'lat': lat, 'long': long, 'loc':Reverse_location(lat,long), 'id':id, 'pw':pw}
    return render(request, 'ToBi/weather.html', data)

def schedule(request):
    id = request.POST['username']
    pw = request.POST['password']
    timetable = eclass.eclass(id,pw)
    data = {'title': 'Schedule', 'id':id, 'pw':pw, 'timetable':timetable}
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


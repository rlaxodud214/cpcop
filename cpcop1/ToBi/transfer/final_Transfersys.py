from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, unquote
from bs4 import BeautifulSoup
from selenium import webdriver
# location.py 파일 필요 -> 딕셔너리의 키는 역이름이고 값은 좌표를 가진 데이터 파일임
import xmltodict, json, urllib, location, requests, time, tabula
import pandas as pd
import hashlib
import hmac
import base64
import requests
import time
import numpy as np
from urllib.parse import urlencode
from urllib.request import urlopen, Request
import urllib
import bs4
import dict_go
# dict_go.py 있어야함 -> 딕셔너리의 키는 시간, 값은 셔틀 분 데이터 값


def IPCall():
    enc_location = urllib.parse.quote("ip 주소 확인")
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html5lib')
    ip = soup.select("div[class=ip_chk_box]")
    name = str(ip[0])
    answer = name[24:]
    array = answer.split("<")
    return array[0]


 Signature Make
def make_signature(method, basestring, timestamp, access_key, secret_key):
    message = method + " " + basestring + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'utf-8')
    signature = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    return signature


def requestApi(timestamp, access_key, signature, uri):
    # Header for Request
    headers = {'x-ncp-apigw-timestamp': timestamp,
               'x-ncp-iam-access-key': access_key,
               'x-ncp-apigw-signature-v2': signature}

    # Geolocation API Request
    res = requests.get(uri, headers=headers)

    # Check Response
    content = res.content.decode(encoding='utf-8')
    content1 = content.split(",")
    content1 = np.array(content1)
    content1[7] = content1[7].replace('"lat": ', '')
    content1[8] = content1[8].replace('"long": ', '')
    return content1[7], content1[8]


def Now_LatNLon():
    method = "GET"
    ipname = IPCall()
    basestring = "/geolocation/v2/geoLocation?ip=" + ipname + "&ext=t&responseFormatType=json"
    timestamp = str(int(time.time() * 1000))
    access_key = "1bl8GtXyTTzXDCG4lgrA"  # access key id (from portal or sub account)
    secret_key = "C43S00RfBboTCIm89TlO8DxqLzChvuLBgr0fO2SD"  # secret key (from portal or sub account)
    secret_key = bytes(secret_key, 'UTF-8')
    signature = make_signature(method, basestring, timestamp, access_key, secret_key)

    # GET Request
    hostname = "https://geolocation.apigw.ntruss.com"
    requestUri = hostname + basestring
    (lat, lon) = requestApi(timestamp, access_key, signature, requestUri)

    return (lat, lon)


 hour = 시간표 시간, Startx = 시작위치.....End
def Span_Time(Near_Station_Lat, Near_Station_Lon):
    url = 'http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoBySubway'
    params = '?' + urlencode({
        quote_plus(
            "serviceKey"): "p%2FjvMYI4C7znYs1z7bwkpbC5XOPhQ2c5XMyRYcH6A%2BLnvRkIO95%2F9tyKecxg06ais5rGNSxsY6eplXsP3%2F%2FiSw%3D%3D",
        quote_plus("startX"): Near_Station_Lat,  # 좌표126.74
        quote_plus("startY"): Near_Station_Lon,  # 37.351828
        quote_plus("endX"): '126.74',  # 정왕역 좌표127.027637
        quote_plus("endY"): '37.351828',  # 37.497950
    })
    url = url + unquote(params)
    req = requests.get(url)
    xpars = xmltodict.parse(req.text)
    dump = json.dumps(xpars)
    data1 = json.loads(dump)
    # pd.DataFrame(data1['ServiceResult']['msgBody']['itemList']['pathList'])
    time = data1['ServiceResult']['msgBody']['itemList']['time']
    return str(time)


def Shuttle_Time_go(hour, minute, dict_go):
    # defhour, defminute이 선언되지 않아서 if문에서 조건을 충족하지 못해서
    # defhour이 원하는 값으로 초기화되지 않은 경우 초기화된 값이 없으므로 return에서 오류(UnboundLocalError) 발생
    defhour = int(hour)
    defminute = int(minute)
    convminute = int(minute) + 60 * int(hour)
    while (True):
        if (8 <= defhour <= 22):
            if (int(dict_go[defhour][0]) + defhour * 60 + 15 > convminute):
                # 셔틀시간+15분이 학교에 도착하는 시간이라는 가정하에,시간대에 가장 이른 셔틀의 도착시간은 defminute보다 크면 안됨,
                defhour -= 1
                # 따라서 defhour을 1 빼주고
                continue
                # defminute를 60으로 설정.
                # 반복문의 맨 처음으로 돌아가게 한다.
            else:
                for i in range(len(dict_go[defhour])):
                    if (convminute >= int(dict_go[defhour][-1 - i]) + defhour * 60 + 15):
                        defminute = dict_go[defhour][-1 - i]
                        return (str(defhour), str(defminute))
                    else:
                        continue
        else:
            return ("err", "err")


def Near_Bus_Station(lat, lon):
    url = 'http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoByBus'
    params = '?' + urlencode({
        quote_plus(
            "serviceKey"): "p%2FjvMYI4C7znYs1z7bwkpbC5XOPhQ2c5XMyRYcH6A%2BLnvRkIO95%2F9tyKecxg06ais5rGNSxsY6eplXsP3%2F%2FiSw%3D%3D",
        quote_plus("startX"): lon,  # 현재위치가 들어갈 곳
        quote_plus("startY"): lat,  # 현재위치가 들어갈 곳
        quote_plus("endX"): location.dict_location[Near_Sub_Station(lat, lon)[:-1]][1],  # 이 좌표는 현재위치로부터 가까운 역인 강남역의 좌표임
        quote_plus("endY"): location.dict_location[Near_Sub_Station(lat, lon)[:-1]][0],
    })
    # print(location.dict_location[Near_Sub_Station(lat,lon)[:-1]][1], location.dict_location[Near_Sub_Station(lat,lon)[:-1]][0], Near_Sub_Station(lat,lon)[:-1])
    url = url + unquote(params)
    req = requests.get(url)
    xpars = xmltodict.parse(req.text)
    dump = json.dumps(xpars)
    data1 = json.loads(dump)

    Travel_time = data1['ServiceResult']['msgBody']['itemList']
    data = pd.DataFrame(Travel_time)
    data['time'] = data['time'].astype('int')
    Travel_time_bus = int(data['time'].mean(axis=0) + 0.5)  # 평균 소요시간
    return Travel_time_bus


def Near_Sub_Station(lat, lon):
    lat = lat  # 한국산업기술대학교 위도("37.340037")
    lon = lon  # 한국산업기술대학교 경도("126.733381")
    key = "l7xx00cd3e8e95cc4fee84f48861b2d6d812"  # api 키
    url = "https://apis.openapi.sk.com/tmap/pois/search/around?version=1"
    queryParams = "&" + urlencode({quote_plus('centerLat'): lat,
                                   quote_plus('centerLon'): lon,
                                   quote_plus('radius'): "0",
                                   quote_plus('categories'): '%EC%A7%80%ED%95%98%EC%B2%A0%EC%97%AD',
                                   quote_plus('appKey'): key})

    request = urllib.request.Request(url + unquote(queryParams))
    request.get_method = lambda: 'GET'

    response_body = urlopen(request).read()
    decode = response_body.decode('utf-8')

    try:
        json_data = json.loads(decode)
        data = json_data['searchPoiInfo']['pois']['poi'][0]['name']
        stloc = data.rfind('역') + 1
        return data[:stloc]
    except:
        return "err"


def eclass(id, password):
    # 크롬창을 띄우지 않는 옵션
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')

    # 위치 지정
    driver = webdriver.Chrome("C:\\ttemp/chromedriver.exe", options=options)

    # 웹 자원 로드를 위해 암묵적으로 딜레이
    delay_time = 3
    driver.implicitly_wait(delay_time)

    # URL 접속 시도
    driver.get('http://eclass.kpu.ac.kr/ilos/main/member/login_form.acl')

    # ID, PW 입력
    # usr_id = input("ID를 입력해주세요 :")
    # usr_pwd = input("PW를 입력해주세요 :")
    # usr_id = "2015162013"
    # usr_pwd = "mouse3178!"
    usr_id = str(id)
    usr_pwd = str(password)
    driver.find_element_by_name('usr_id').send_keys(usr_id)
    driver.find_element_by_name('usr_pwd').send_keys(usr_pwd)

    # 로그인 버튼 클릭
    driver.find_element_by_xpath('//*[@id="myform"]/div/div/div/div').click()

    # URL 접속 시도
    driver.get("http://eclass.kpu.ac.kr/ilos/main/main_form.acl")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # notices = driver.find_element_by_class_name('title-01').text
    # print(notices)

    # notices = soup.select('div.p_inr > div.p_info > a > span')
    name1 = soup.select('div > ol > li > em')
    time1 = soup.select('div > ol > li > span')

    eclass = []
    for item in zip(name1, time1):
        eclass.append(
            {
                'name': item[0].text.replace('\n', '').strip(),
                'time': item[1].text.replace('\n', '').strip()
            }
        )

    data = pd.DataFrame(eclass)
    index = 0
    dict1 = {}
    for i, ch in enumerate(data['name']):
        data['name'][i] = data['name'][i][:-42]

    for i, ch in enumerate(data['time']):
        if (ch[0] not in ['월', '화', '수', '목', '금']):
            index = i
            break

    data.drop(data.index[index::], inplace=True)

    dict1 = {}
    weeks = ['월', '화', '수', '목', '금']
    for i, ch in enumerate(data['time']):
        for j in range(len(data['time'][i])):
            if ch[j] in weeks:
                data['time'][i] = ch.strip()
                if ch[j] not in dict1:
                    dict1[ch[j]] = list()  # ch[j]키가 없을떈 빈리스트를 value로 하고, ch[j]를 키값으로 하는 요소생성
                if len(data['time'][i]) > 31:  # 일주일에 2번 나눠서 수업
                    if j > 1:
                        dict1[data['time'][i][0:j][0]].append(data['time'][i][0:j])
                        dict1[ch[j]].append(data['time'][i][j:])
                else:  # 일주일에 1타임만 수업
                    dict1[ch[j]].append(data['time'][i])

    for ch in weeks:
        for i in range(len(dict1[ch])):
            list2 = dict1[ch][i].split(' ')
            if list2[2] != '':
                dict1[ch][i] = list2[2]
            else:
                dict1[ch][i] = list2[5]
        dict1[ch] = sorted(dict1[ch])

    dict2 = {}

    for ch in weeks:
        dict2[ch] = dict1[ch][0][0:5]
        dict2[ch] = {'hour': int(dict2[ch][0:2]), 'minute': int(dict2[ch][3:5])}

    return dict2


def Sub_Time(hour, minute, inja):
    cm = hour * 60 + minute - inja
    h = cm // 60
    m = cm % 60
    return h, m

start = time.time()
dictgo = dict_go.dict_time_table_go
now_location = ['37.491575', '127.030912']
 now_location = Now_LatNLon()
nearsub1 = Near_Sub_Station(now_location[0], now_location[1])  # 좌표(현재 위치) -> 정왕역 (좌표로 부터 가까운 역 검색)
rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks))
index1 = nearsub1.rstrip('역')  # 정왕역 -> 정왕
 n = time.localtime().tm_wday
n = 1
weeks = ['월', '화', '수', '목', '금']
 print(weeks[n])
 data = int(eclass("2015162013", 'mouse3178!')[weeks[n]])
data = eclass("2019152025", 'su9191su?k')[weeks[n]]
h1 = int(data['hour'])
m1 = int(data['minute'])
rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks))
temp = rjfflstlrks

std = Shuttle_Time_go(h1, m1, dictgo)
h2 = int(std[0])
m2 = int(std[1])
rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks-temp))
temp = rjfflstlrks

dict1 = {}
dict1['starty'], dict1['startx'] = location.dict_location[index1]  # 정왕 -> 정왕역 좌표 [37.351735, 126.742989] (역이름으로 좌표 반환)
time_info = Span_Time(dict1['startx'], dict1['starty'])
h3, m3 = Sub_Time(h2, m2, int(time_info))
rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks-temp))
temp = rjfflstlrks

Travel_time_bus = Near_Bus_Station(now_location[0], now_location[1])
h4, m4 = Sub_Time(h3, m3, Travel_time_bus)
rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks-temp))
temp = rjfflstlrks

h5, m5 = Sub_Time(h4, m4, 10)
print("출발 시스템"+"-"*60)
print("현재 " + str(now_location) + "의 위치에서 가장 가까운 역은 " + str(index1) + "역입니다.\n")
print("출발 추천시간 (집-> 버스정류장) : " + str(h5) + "시 " + str(m5) + "분(예상소요시간 : 10분)\n")
if Travel_time_bus > 4:
    print("버스정류장->%s역 : %s시 %s분(예상소요시간 : %s분)" % (index1, str(h4), str(m4), str(Travel_time_bus)))
print(nearsub1 + "에서 출발해야하는 시간 : " + str(h3) + "시 " + str(m3) + "분(예상소요시간 : " + time_info + "분)")
print("정왕역에서 출발하는 " + str(h2) + "시 " + str(m2) + "분 셔틀 탑승")
print("학교에 도착해야하는 시간 : %d시 %d분 (시간표 정보 읽어오기)\n" % (h1, m1))
rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks))

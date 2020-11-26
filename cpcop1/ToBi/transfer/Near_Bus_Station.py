from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, unquote
from bs4 import BeautifulSoup
from selenium import webdriver
# location.py 파일 필요 -> 딕셔너리의 키는 역이름이고 값은 좌표를 가진 데이터 파일임
import xmltodict, json, urllib, requests, time, tabula
import ToBi.transfer.location as location
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
import ToBi.transfer.dict_go as dict_go

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
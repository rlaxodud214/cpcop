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
# dict_go.py 있어야함 -> 딕셔너리의 키는 시간, 값은 셔틀 분 데이터 값


def Near_Sub_Station(lat, lon):
    lat = lat  # 한국산업기술대학교 위도("37.340037")
    lon = lon  # 한국산업기술대학교 경도("126.733381")
    key = "l7xx00cd3e8e95cc4fee84f48861b2d6d812"  # api 키
    url = "https://apis.openapi.sk.com/tmap/pois/search/around?version=1"
    queryParams = "&" + urlencode({quote_plus('centerLat'): lat,
                                   quote_plus('centerLon'): lon,
                                   quote_plus('radius'): "0",
                                   quote_plus('categories'): '%EC%A7%80%ED%95%98%EC%B2%A0%EC%97%AD',  # 지하철역
                                   quote_plus('appKey'): key})

    request = urllib.request.Request(url + unquote(queryParams))
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    decode = response_body.decode('utf-8')

    try:
        json_data = json.loads(decode)
        data = json_data['searchPoiInfo']['pois']['poi'][0]['name']
        stloc = data.rfind("역") + 1
        # query = parse.quote(data[:stloc])
        # return str(query)[0:-9]
        # print(url+unquote(queryParams))
        return data[:stloc]
    except:
        return "err"
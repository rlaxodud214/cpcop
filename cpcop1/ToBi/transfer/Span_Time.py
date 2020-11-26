from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, unquote
from bs4 import BeautifulSoup
from selenium import webdriver
# location.py 파일 필요 -> 딕셔너리의 키는 역이름이고 값은 좌표를 가진 데이터 파일임
import xmltodict, json, urllib, requests, time, tabula
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

from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, unquote
from bs4 import BeautifulSoup
from selenium import webdriver
# Gpss.py 파일 필요 -> 딕셔너리의 키는 역이름이고 값은 좌표를 가진 데이터 파일임
import xmltodict, json
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
import Traffic.SubDIct
import Traffic.NearStation
import Traffic.SuttleDict
import Traffic.SubTime
import Traffic.ShuttleTimeGo
import Traffic.SpanTime
import Util.Eclass



start = time.time()
dictgo = Traffic.SuttleDict.timetableGo
now_location = ['37.491575', '127.030912']
# now_location = Now_LatNLon()
nearsub1 = Traffic.NearStation.nearSubStation(now_location[0], now_location[1])  # 좌표(현재 위치) -> 정왕역 (좌표로 부터 가까운 역 검색)
index1 = nearsub1.rstrip('역')  # 정왕역 -> 정왕
# n = time.localtime().tm_wday
n = 1
weeks = ['월', '화', '수', '목', '금']
# print(weeks[n])
# data = int(class("2015162013", 'mouse3178!')[weeks[n]])
data = Util.Eclass.eclass("2019152025", 'su9191su?k')[1][weeks[n]]
h1 = int(data['hour'])
m1 = int(data['minute'])
std = Traffic.ShuttleTimeGo.shuttleTimeGo(h1, m1, dictgo)
h2 = int(std[0])
m2 = int(std[1])
dict1 = {}
dict1['starty'], dict1['startx'] = Traffic.SubDIct.subDict[index1]  # 정왕 -> 정왕역 좌표 [37.351735, 126.742989] (역이름으로 좌표 반환)
time_info = Traffic.SpanTime.spanTime(dict1['startx'], dict1['starty'])
h3, m3 = Traffic.SubTime.subTime(h2, m2, int(time_info))
Travel_time_bus = Traffic.NearStation.nearBusStation(now_location[0], now_location[1])
h4, m4 = Traffic.SubTime.subTime(h3, m3, Travel_time_bus)
h5, m5 = Traffic.SubTime.subTime(h4, m4, 10)
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


from django.shortcuts import render

import ToBi.transfer.eclass as eclass
import ToBi.Weather.WeatherZip as Weather
import ToBi.Weather.NaverWeather as naver
import ToBi.Util.Gpss as GPS
from ast import literal_eval
import json
import pandas as pd

def login(request):
    return render(request, 'login.html')

def index(request):
    try:
        id = request.POST['username']
        pw = request.POST['password']
        data = {'월':[[]], '화':[[]], '수':[[]], '목':[[]], '금':[[]]}
        try:
            data.update(eclass.eclass1(id,pw))
        except:
            return render(request, 'Error.html', data)
        return render(request, 'index.html',data)
    except:
        Mon = request.POST['Monday']
        Tue = request.POST['Tuesday']
        Wed = request.POST['Wednesday']
        Thu = request.POST['Thursday']
        Fri = request.POST['Friday']
        data = {'title': 'ToBi', '월': Mon, '화': Tue, '수': Wed, '목': Thu, '금': Fri}
        return render(request, 'index.html', data)

def traffic(request):
    Mon = request.POST['Monday']
    Tue = request.POST['Tuesday']
    Wed = request.POST['Wednesday']
    Thu = request.POST['Thursday']
    Fri = request.POST['Friday']
    loc = request.POST['fixed_loc']
    data = {'title': 'Traffic',  '월':Mon, '화':Tue, '수':Wed, '목':Thu, '금':Fri, 'loc':loc}
    return render(request, 'ToBi/traffic.html', data)

def weather(request):
    Mon = request.POST['Monday']
    Tue = request.POST['Tuesday']
    Wed = request.POST['Wednesday']
    Thu = request.POST['Thursday']
    Fri = request.POST['Friday']
    loc = request.POST['fixed_loc']
    #loc = GPS.reverseLocation(lat,lon)
    loc_name = loc.split(',')
    data = naver.naverWeather(loc_name[0], loc_name[1])
    temp = data[0]
    maxtemp = data[1]
    mintemp = data[2]
    rep = data[5]
    wds = data[6]
    rain = data[3]
    howrain = data[4]
    data = {'title': 'Weather', '월':Mon, '화':Tue, '수':Wed, '목':Thu, '금':Fri, 'temp':temp, 'maxtemp':maxtemp, 'mintemp':mintemp,
            'rep':rep, 'wds':wds,'rain':rain, 'howrain':howrain, "loc":loc, 'loc_name':GPS.reverseLocation(loc_name[0],loc_name[1])}
    return render(request, 'ToBi/weather.html', data)

def schedule(request):
    Mon1 = request.POST['Monday']
    Tue1 = request.POST['Tuesday']
    Wed1 = request.POST['Wednesday']
    Thu1 = request.POST['Thursday']
    Fri1 = request.POST['Friday']
    loc = request.POST['fixed_loc']
    data = {'월': literal_eval(Mon1), '화':literal_eval(Tue1), '수':literal_eval(Wed1), '목':literal_eval(Thu1), '금':literal_eval(Fri1)}
    Mon = ['', '', '', '', '', '', '', '', '', '', '', '']
    Mon_time = ['Mon_1','Mon_2','Mon_3','Mon_4','Mon_5','Mon_6','Mon_7','Mon_8','Mon_9','Mon_10','Mon_11','Mon_12']
    Tue = ['', '', '', '', '', '', '', '', '', '', '', '']
    Tue_time = ['Tue_1', 'Tue_2', 'Tue_3', 'Tue_4', 'Tue_5', 'Tue_6', 'Tue_7', 'Tue_8', 'Tue_9', 'Tue_10', 'Tue_11','Tue_12']
    Wed = ['', '', '', '', '', '', '', '', '', '', '', '']
    Wed_time = ['Wed_1', 'Wed_2', 'Wed_3', 'Wed_4', 'Wed_5', 'Wed_6', 'Wed_7', 'Wed_8', 'Wed_9', 'Wed_10', 'Wed_11','Wed_12']
    Thu = ['', '', '', '', '', '', '', '', '', '', '', '']
    Thu_time = ['Thu_1', 'Thu_2', 'Thu_3', 'Thu_4', 'Thu_5', 'Thu_6', 'Thu_7', 'Thu_8', 'Thu_9', 'Thu_10', 'Thu_11','Thu_12']
    Fri = ['', '', '', '', '', '', '', '', '', '', '', '']
    Fri_time = ['Fri_1', 'Fri_2', 'Fri_3', 'Fri_4', 'Fri_5', 'Fri_6', 'Fri_7', 'Fri_8', 'Fri_9', 'Fri_10', 'Fri_11','Fri_12']
    list = ['월', '화', '수', '목', '금']
    time = ['09:30', '10:30', '11:30', '12:30', '13:30', '14:30', '15:30', '16:30', '17:25', '18:15', '19:15', '19:55']
    end = ['10:20', '11:20', '12:20', '13:20', '14:20', '15:20', '16:20', '17:20', '18:15', '19:5', '19:55', '']
    for i in range(len(list)):
        if (data[list[i]] != [[]]):
            for j in range(len(data[list[i]])):
                touch = data[list[i]][j][1].split('~')
                for p in range(len(time)):
                    if (touch[0] == time[p]):
                        if (list[i] == '월'):
                            for k in range(p, len(time), 1):
                                Mon[k] = data[list[i]][j][0]
                                if (touch[1] == end[k]):
                                    break
                        if (list[i] == '화'):
                            for k in range(p, len(time), 1):
                                Tue[k] = data[list[i]][j][0]
                                if (touch[1] == end[k]):
                                    break
                        if (list[i] == '수'):
                            for k in range(p, len(time), 1):
                                Wed[k] = data[list[i]][j][0]
                                if (touch[1] == end[k]):
                                    break
                        if (list[i] == '목'):
                            for k in range(p, len(time), 1):
                                Thu[k] = data[list[i]][j][0]
                                if (touch[1] == end[k]):
                                    break
                        if (list[i] == '금'):
                            for k in range(p, len(time), 1):
                                Fri[k] = data[list[i]][j][0]
                                if (touch[1] == end[k]):
                                    break

    data = {'title': 'Schedule', 'loc':loc, 'Mon':Mon1, 'Tue':Tue1, 'Wed':Wed1, 'Thu':Thu1, 'Fri':Fri1}
    data1 = dict(zip(Mon_time,Mon))
    data2 = dict(zip(Tue_time,Tue))
    data3 = dict(zip(Wed_time,Wed))
    data4 = dict(zip(Thu_time,Thu))
    data5 = dict(zip(Fri_time,Fri))
    data.update(data1)
    data.update(data2)
    data.update(data3)
    data.update(data4)
    data.update(data5)
    return render(request, 'ToBi/schedule.html', data)

def error(request):
    loc = request.POST['fixed_loc']
    data = {'title': 'error', 'loc': loc}
    return render(request, 'Error.html', data)

# print(Weather.weatherZip(lat, lon), type(Weather.weatherZip(lat,lon)), '\n\n')


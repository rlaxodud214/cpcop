from django.shortcuts import render

import ToBi.transfer.eclass as eclass
import ToBi.Weather.WeatherZip as Weather
import ToBi.Util.Gpss as GPS
import ToBi.Weather.NaverWeather as naver

def login(request):
    return render(request, 'login.html')

def index(request):
    try:
        id = request.POST['username']
        pw = request.POST['password']
        data = {'월':[[]], '화':[[]], '수':[[]], '목':[[]], '금':[[]]}
        data.update(eclass.eclass1(id,pw))
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
    #loc = GPS.reverseLocation(lat, lon)
    #print(loc)
    print(lat, lon)
    data = {'title': 'Traffic',  '월':Mon, '화':Tue, '수':Wed, '목':Thu, '금':Fri}
    return render(request, 'ToBi/traffic.html', data)

def weather(request):
    Mon = request.POST['Monday']
    Tue = request.POST['Tuesday']
    Wed = request.POST['Wednesday']
    Thu = request.POST['Thursday']
    Fri = request.POST['Friday']
    lat = GPS.location()[0]
    lon = GPS.location()[1]
    #loc = GPS.reverseLocation(lat,lon)
    data = naver.naverWeather("37.3398", "126.7335")
    temp = data[0]
    maxtemp = data[1]
    mintemp = data[2]
    rep = data[5]
    wds = data[6]
    rain = data[3]
    howrain = data[4]
    data = {'title': 'Weather', '월':Mon, '화':Tue, '수':Wed, '목':Thu, '금':Fri, 'temp':temp, 'maxtemp':maxtemp, 'mintemp':mintemp,
            'rep':rep, 'wds':wds,'rain':rain, 'howrain':howrain}
    return render(request, 'ToBi/weather.html', data)

def schedule(request):
    Mon = request.POST['Monday']
    Tue = request.POST['Tuesday']
    Wed = request.POST['Wednesday']
    Thu = request.POST['Thursday']
    Fri = request.POST['Friday']
    data = {'title': 'Schedule', '월':Mon, '화':Tue, '수':Wed, '목':Thu, '금':Fri}
    return render(request, 'ToBi/schedule.html', data)


lat = GPS.location()[0]
lon = GPS.location()[1]
# print(Weather.weatherZip(lat, lon), type(Weather.weatherZip(lat,lon)), '\n\n')


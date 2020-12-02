from django.shortcuts import render

import ToBi.transfer.eclass as eclass
import ToBi.Weather.WeatherZip as Weather
import ToBi.Weather.NaverWeather as naver
import ToBi.Util.Gpss as GPS

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
    Mon = request.POST['Monday']
    Tue = request.POST['Tuesday']
    Wed = request.POST['Wednesday']
    Thu = request.POST['Thursday']
    Fri = request.POST['Friday']
    loc = request.POST['fixed_loc']
    data = {'title': 'Schedule', '월':Mon, '화':Tue, '수':Wed, '목':Thu, '금':Fri, 'loc':loc}
    return render(request, 'ToBi/schedule.html', data)

def error(request):
    loc = request.POST['fixed_loc']
    data = {'title': 'error', 'loc': loc}
    return render(request, 'Error.html', data)

# print(Weather.weatherZip(lat, lon), type(Weather.weatherZip(lat,lon)), '\n\n')


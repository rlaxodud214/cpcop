from django.shortcuts import render

import ToBi.transfer.eclass as eclass
import ToBi.Weather.WeatherZip as Weather
import ToBi.Util.Gpss as GPS

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
    temp = Weather.weatherZip(lat,lon)['현재온도']
    maxtemp = Weather.weatherZip(lat, lon)['최고온도']
    mintemp = Weather.weatherZip(lat, lon)['최저온도']
    rain = Weather.weatherZip(lat,lon)['비올확률']
    howrain = Weather.weatherZip(lat,lon)['강수량']

    data = {'title': 'Weather', '월':Mon, '화':Tue, '수':Wed, '목':Thu, '금':Fri, 'temp':temp, 'maxtemp':mintemp, 'maxtemp':mintemp,
            'rain':rain, 'howrain':howrain}
    return render(request, 'ToBi/weather.html', data)

def schedule(request):
    Mon = request.POST['Monday']
    Tue = request.POST['Tuesday']
    Wed = request.POST['Wednesday']
    Thu = request.POST['Thursday']
    Fri = request.POST['Friday']
    data = {'title': 'Schedule', '월':Mon, '화':Tue, '수':Wed, '목':Thu, '금':Fri}
    return render(request, 'ToBi/schedule.html', data)







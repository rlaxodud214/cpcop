from urllib.parse import urlencode, unquote, quote_plus
import ToBi.Util.Gpss
import json, math, datetime, pytz, requests
import pandas as pd

# 현재 시간에서 1시간씩 빼면서 기상청이 데이터를 갱신해주는 시간을 찾아서 반환해주는 코드 / 다른 .py파일에서의 사용 x / 매개값 : 없음 / 리턴값 : str타입 (20201102, 2200)
def timeInfo():
    standard_time = [2, 5, 8, 11, 14, 17, 20, 23] # 기상청이 데이터 갱신해주는 시간
    time_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H') #현재 서울의 시간 ex)11, 22
    check_time = int(time_now) - 1 #현재 시간에서 1시간 뺀 값 ex) 21 - 1 = 20시 이유 : 데이터가 40분에 업데이트 돼서 ex) 21시 40분

    day_calibrate = 0
    while not check_time in standard_time : # 기상청이 데이터 갱신해주는 시간과 같을때까지 현재시간 =- 1
        check_time -= 1
        if check_time < 2 : # 만약 2시보다 작다면 그 전인 23시의 데이터를 받아와야 하므로
            day_calibrate = 1  # 이후 날짜의 계산에서 하루전으로 만들어주려고 나중에 1을 빼면 되므로 1을 저장
            check_time = 23    # 2시 이전의 standard_time은 23시 이므로 그냥 값을 줘버림

    date_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')  #현재 시간의 년도, 월, 일 ex) 20200101
    check_date = int(date_now) - day_calibrate #만약 02시 이전이여서 day_calibrate이 값이 1로 됐으면 날짜를 하루 빼줘야하므로
    if check_time < 10:
        return (str(check_date), ('0' + str(check_time) + '00'))  # ex) (20200109, 시각00) 00을 붙이는 이유는 api에서 데이터의 값으로 2200을 요구해서이다.
    else:
        return (str(check_date), (str(check_time) + '00'))  # ex) (20200109, 시각00) 00을 붙이는 이유는 api에서 데이터의 값으로 2200을 요구해서이다.

# 강수형태 -> 차후 겨울에 눈올때 서비스 예정이긴 한데 이미지 파일로 대체도 가능 / 다른 .py파일에서의 사용 x / PTY는 강수타입을 말하는 거임 강수타입인 key값에 따라 value값을 반환 현재 사용X 차후 필요시 개발
def rainType(PTY):
    dict = {'0': '없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기', '5': '빗방울', '6': '빗방울/눈날림', '7': '눈날림'}
    return dict[PTY]

# 일반적인 좌표값을 기상청의 격자 좌표로 변경해주는 코드 / 다른 .py파일에서의 사용 x / 매개값 : float타입 (37.339873, 136.733557) / 반환값 : int타입 (228, 134)
def mapToGrid(lat, lon, code=0):
    NX = 149  ## X축 격자점 수
    NY = 253  ## Y축 격자점 수

    Re = 6371.00877  ##  지도반경
    grid = 5.0  ##  격자간격 (km)
    slat1 = 30.0  ##  표준위도 1
    slat2 = 60.0  ##  표준위도 2
    olon = 126.0  ##  기준점 경도
    olat = 38.0  ##  기준점 위도
    xo = 210 / grid  ##  기준점 X좌표
    yo = 675 / grid  ##  기준점 Y좌표
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI / 180.0
    RADDEG = 180.0 / PI

    re = Re / grid
    slat1 = slat1 * DEGRAD
    slat2 = slat2 * DEGRAD
    olon = olon * DEGRAD
    olat = olat * DEGRAD

    sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(PI * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(PI * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)

    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI:
        theta -= 2.0 * PI
    if theta < -PI:
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    # print(lat, lon, x, y)
    return x, y

# 좌표를 입력받아 getdata에 넘겨줘서 데이터를 수집하고 이 메소드에선 데이터 처리만함 / 다른 .py파일에서의 사용 x
# / 매개값 : float타입 ('37.518393', '126.737572', '37.339873', '126.733557', )
# / 반환값 : str타입 ('4', 9.5, -4.0, 1.3333333333333333, '0', '81', '4', (14.0, '0'), (12.666666666666666, '0'))
def korWeather(school_location1, school_location2, home_location1, home_location2):

    # Setting for URL parsing
    url1 = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst'
    data1 = getData(url1, home_location1, home_location2)
    url2 = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'
    data2 = getData(url2, home_location1, home_location2)     # 집의 날씨 예보
    data3 = getData(url2, school_location1, school_location2) # 학교의 날씨 예보

    dict1 = {}
    dict2 = {}
    if str(type(data2)) == "<class 'str'>" or str(type(data1)) == "<class 'str'>":
        # print("오류가났습니다")
        return "오류가났습니다"

    else:
        df_sample = data1[['category', 'obsrValue']]
        df_sample.index = df_sample['category']
        data11 = df_sample['obsrValue']
        dict1 = data11.to_dict()


        df = data2[['category', 'fcstTime', 'fcstValue']]
        #  6시간 강수량     온도      습도      풍속     강수확률      6시간 강수량     최고기온   최저기온
        save_category = ['R06', 'T3H', 'REH', 'WSD', 'POP', 'R06', 'TMX', 'TMN']
        save_index = [i for i, ch in enumerate(df['category']) for j in save_category if ch == j]
        data22 = df.iloc[save_index]
        data22.index = range(len(data22))  # 인덱스 재정의

        for ch in save_category:
            tmp = data22.loc[data22.category == ch].fcstValue
            tmp.index = range(len(tmp))
            tmp = tmp.to_dict()
            dict2[ch] = tmp
            # print(ch, dict2[ch])
            sum = 0.0
            for i in range(len(dict2[ch])):
                sum += float(dict2[ch][i])
                if i>=5: break
            dict2[ch] = sum/len(dict2[ch])
        # print(dict1, '\n', dict2, '\n')

        return (dict1['T1H'], dict2['TMX'], dict2['TMN'], dict2['POP'], dict1['RN1'], dict1['REH'], dict1['WSD'])

# url과 좌표를 이용해서 data를 가져오는 코드  /  다른 .py파일에서의 사용 x /  이하 매개값 str 타입
# http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst 37.339873 126.733557
# http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst 37.339873 126.733557
# http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst 37.518393 126.737572
# 반환값 DataFrame타입 :    baseDate baseTime category  nx   ny obsrValue
# 0  20201120     0800      PTY  56  122         0
# 1  20201120     0800      REH  56  122        70
#      baseDate baseTime category  fcstDate fcstTime fcstValue  nx   ny
# 0    20201120     0800      POP  20201120     1200        30  56  122
# 1    20201120     0800      PTY  20201120     1200         0  56  122
def getData(url, location1, location2):
    base = timeInfo()
    narray = mapToGrid(float(location1), float(location2))
    params = '?' + urlencode({
        quote_plus("serviceKey"): "p%2FjvMYI4C7znYs1z7bwkpbC5XOPhQ2c5XMyRYcH6A%2BLnvRkIO95%2F9tyKecxg06ais5rGNSxsY6eplXsP3%2F%2FiSw%3D%3D",     # 인증키
        quote_plus("numOfRows"): "150",  # 한 페이지 결과 수 // default : 10
        quote_plus("pageNo"): "1",  # 페이지 번호 // default : 1
        quote_plus("dataType"): "JSON",  # 응답자료형식 : XML, JSON
        quote_plus("base_date"): base[0],  # 발표일자 // yyyymmdd  20201103
        quote_plus("base_time"): base[1],  # 발표시각 // HHMM, 매 시각 40분 이후 호출
        quote_plus("nx"): narray[0],  # 예보지점 X 좌표
        quote_plus("ny"): narray[1]  # 예보지점 Y 좌표
    })

    try:
        url = url + unquote(params)
        req = requests.get(url).content  # url로 데이터 추출함 - 바이트타입 추출
        data1 = json.loads(req)  # 위에서 뽑은 바이트타입 데이터를 딕셔너리로 변경해주는 코드
        # print(data1['response']['body']['items']['item'])
        data = pd.DataFrame(data1['response']['body']['items']['item'])
    except KeyError:
        data = "KeyError에러 getdata()에 base_time 파라미터값 오류" + str(base) + "\n"
    except json.decoder.JSONDecodeError:
        data = "json.decoder.JSONDecodeError 에러 발생 이유 찾는 중..." + str(base) + "\n"
    except:
        data = "KeyError에러 getdata()에 base_time 파라미터값 오류" + str(base) + "\n"

    # print(data)
    return data

if __name__ == "__main__":
    # location = Util.gpss.main()  # location = [0] : 정왕1동, [1] : 37.340288, [2] : 126.743981 튜플반환
    # print('<현재 위치의 날씨정보>\n' + korWeather(location[1], location[2])) # gps값 들어갈 곳
    # print(korWeather('37.339873', '136.733557'))  # 임시 위치 - 데이터 확인용
    print(korWeather('37.518393', '126.737572', '37.339873', '126.733557'))  # 학교 위치
    #('37.339873', '126.733557')   #학교 좌표 위경도 값 - 구글에서 따옴
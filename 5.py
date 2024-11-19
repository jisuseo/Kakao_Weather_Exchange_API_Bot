import requests

apikey = "e2656af1c02f7c2f65d82ce7285d4f2b"
city = "Dusseldorf"
lang = "kr"
full_url = f"http://api.openweathermap.org/data/2.5/forecast?id=524901&q={city}&appid={apikey}&lang={lang}&units=metric"
response_org = requests.get(full_url).json()
print(response_org['list'])
print("#############################################\n\n")
print(response_org['list'][0])
print("현재 시간: \t", response_org['list'][0]['dt_txt'])
print("온도: \t\t", response_org['list'][0]['main']['temp'])
print("체감 온도: \t", response_org['list'][0]['main']['feels_like'])
print("최저 온도: \t", response_org['list'][0]['main']['temp_min'])
print("최고 온도: \t", response_org['list'][0]['main']['temp_max'])
print("습도: \t\t", response_org['list'][0]['main']['humidity'])
print("기압: \t\t", response_org['list'][0]['main']['pressure'])
print("평균 대기압: 약 1013 hPa /// 1000hPa이하는 저기압 분류됨")
print("하늘: \t\t", response_org['list'][0]['weather'][0]['description'])
print("##############################################\n\n")

import os

if os.path.isfile('weather.csv'):
    os.remove('weather.csv')

w_list = []
print("시간\t\t\t", "온도\t", "최저\t", "최고\t", "기압\t\t", "습도\t", "날씨\t" )
for i in response_org['list']:
    print(i['dt_txt'], "\t", i['main']['temp'], "\t", i['main']['temp_min'], "\t", i['main']['temp_max'], "\t", i['main']['pressure'], "(1013 hPa)///1000hPa이하는 저기압 분류됨", "\t\t", i['main']['humidity'], "\t", i['weather'][0]['description'])
    # 리스트 변수에 담아두기
    w_list.append(str(i['dt_txt']) + "," +
                str(i['main']['temp']) + "," +
                str(i['main']['temp_min']) + "," +
                str(i['main']['temp_max']) + "," +
                str(i['main']['pressure']) + "," +
                str(i['main']['humidity']) + "," +
                str(i['weather'][0]['description']) )

    # 파일에 쓰기
    with open('weather.csv', 'a', encoding='utf-8-sig') as f:  # 쓰기
        f.write(str(i['dt_txt']) + "," +
                str(i['main']['temp']) + "," +
                str(i['main']['temp_min']) + "," +
                str(i['main']['temp_max']) + "," +
                str(i['main']['pressure']) + "," +
                str(i['main']['humidity']) + "," +
                str(i['weather'][0]['description']) + "\n")

print("++++++++++++++++++++++++++++++")
print(w_list)

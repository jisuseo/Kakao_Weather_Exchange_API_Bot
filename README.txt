https://openweathermap.org/current

- API call
https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}

http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API key}
url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={apikey}"


https://foss4g.tistory.com/1624


-- 5.py
 # 파일 생성 시 'w' -> 'a'로 설정해야 파일에 값이 모두 쓰여집니다.
# 'w' 모드로 할 경우, 마지막 값으로 덮어쓰기 되기 때문에 마지막 값만 보입니다.
with open('weather.csv', 'a', encoding='utf-8-sig') as f:  # 쓰기
    f.write(str(i['dt_txt']) + "," +
            str(i['main']['temp']) + "," +
            str(i['main']['temp_min


-- 5.py
# csv 파일 생성시 마지막 description의 한글이 깨져서 나오는 경우가 있으므로 utf-8-sig 로 인코딩을 하면 해결됩니다


https://pagichacha.tistory.com/96


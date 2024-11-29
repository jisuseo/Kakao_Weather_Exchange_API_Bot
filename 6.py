import requests

apikey = ""
city = ""
lang = "kr"

url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={apikey}"
# url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={apikey}&lang={lang}"

result = requests.get(url)
print(result.text,type(result.text), "\n\n")

response = requests.get(url).json()
print(response, type(response), "\n\n")


#list로

print(response[0]['name'])
print(response[0]['lat'])
print(response[0]['lon'])


lat = response[0]['lat']
lon = response[0]['lon']

full_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&lang={lang}&units=metric"

response_org = requests.get(full_url).json()
print(response_org)

print(response_org["name"], "의 날씨입니다.")
print("날씨 : ", response_org["weather"][0]["description"])
print("현재 온도 : ", response_org["main"]["temp"])
print("체감 온도 : ", response_org["main"]["feels_like"])
print("최저 기온 : ", response_org["main"]["temp_min"])
print("최고 기온 : ", response_org["main"]["temp_max"])
print("습도 : ", response_org["main"]["humidity"])
print("기압 : ", response_org["main"]["pressure"])
print("풍향 : ", response_org["wind"]["deg"])
print("풍속 : ", response_org["wind"]["speed"])

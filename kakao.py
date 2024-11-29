import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = ""  # OpenWeatherMap API Key
CITY = "Dusseldorf"
LANG = "kr"  # 한국어로 날씨 정보 받기
KAKAO_API_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

@app.route('/weather', methods=['POST'])
def weather():
    # 날씨 정보 가져오기
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&lang={LANG}&units=metric"
    response = requests.get(weather_url).json()

    # 날씨 메시지 생성
    weather_message = f"{CITY}의 날씨입니다.\n"
    weather_message += f"날씨: {response['weather'][0]['description']}\n"
    weather_message += f"온도: {response['main']['temp']}°C\n"
    weather_message += f"최고 기온: {response['main']['temp_max']}°C\n"
    weather_message += f"최저 기온: {response['main']['temp_min']}°C\n"
    
    # 카카오톡 메시지 전송
    send_message(weather_message)
    
    return jsonify({"message": "Weather sent to KakaoTalk!"})

def send_message(message):
    headers = {
        "Authorization": "Bearer <KAKAO_ACCESS_TOKEN>"  # 카카오톡 API 토큰
    }
    data = {
        "template_object": {
            "object_type": "text",
            "text": message,
            "link": {
                "web_url": "http://weather.example.com"
            }
        }
    }
    
    response = requests.post(KAKAO_API_URL, headers=headers, json=data)
    print(response.json())

if __name__ == '__main__':
    app.run(debug=True)

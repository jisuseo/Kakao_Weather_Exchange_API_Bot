# -*- coding: utf-8 -*-

import requests
import datetime
import json
import urllib3
import zoneinfo
import os
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env file
load_dotenv()

# User settings (환경 변수에서 불러오기)
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_REFRESH_TOKEN = os.getenv("KAKAO_REFRESH_TOKEN")
FRIEND_UUID = os.getenv("FRIEND_UUID")
EXIM_API_KEY = os.getenv("EXIM_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

WEEKDAY_KO = ['월', '화', '수', '목', '금', '토', '일']
WEEKDAY_EN_TO_KO = {
    'Mon': '월', 'Tue': '화', 'Wed': '수', 'Thu': '목', 'Fri': '금', 'Sat': '토', 'Sun': '일'
}
WEATHER_KO_EMOJI = {
    "clear sky": "☀️ 맑음",
    "few clouds": "🌤️ 구름 조금",
    "scattered clouds": "🌥️ 구름 약간",
    "broken clouds": "☁️ 구름 많음",
    "overcast clouds": "☁️ 흐림",
    "light rain": "🌦️ 약한 비",
    "moderate rain": "🌧️ 비",
    "heavy intensity rain": "⛈️ 강한 비",
    "light snow": "🌨️ 약한 눈",
    "snow": "❄️ 눈",
    "mist": "🌫️ 안개",
    "fog": "🌁 짙은 안개"
}
def get_temp_emoji(temp):
    if temp <= 0:
        return "🥶"
    elif temp <= 10:
        return "😨"
    elif temp <= 20:
        return "🙂"
    elif temp <= 30:
        return "😎"
    elif temp <= 40:
        return "🥵"
    else:
        return "🔥"

def get_humidity_emoji(humidity):
    if humidity <= 30:
        return "💧"  # 건조
    elif humidity <= 60:
        return "💦"  # 적정
    elif humidity <= 80:
        return "🌊"  # 습함
    else:
        return "🌧️"  # 매우 습함

    
#🔨1️⃣2️⃣3️⃣4️⃣🔥😊📌✅🚨❗🔴🆘📢📣🔔🚨🛑💥❌➡️✔️📝📅
def translate_weather(desc):
    return WEATHER_KO_EMOJI.get(desc, desc)

def refresh_access_token():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": KAKAO_REST_API_KEY,
        "refresh_token": KAKAO_REFRESH_TOKEN
    }
    try:
        response = requests.post(url, data=data)
        return response.json().get("access_token")
    except Exception as e:
        print("Token refresh error:", e)
        return None

def get_exchange_rate():
    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    now_kst = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9)))
    
    search_date = now_kst.date()
    max_lookback_days = 7  # 최대 7일 전까지 탐색
    data_found = False
    data_date = None
    base_data = []
    prev_data = []

    for delta in range(max_lookback_days):
        check_date = search_date - datetime.timedelta(days=delta)
        params = {
            "authkey": EXIM_API_KEY,
            "searchdate": check_date.strftime("%Y%m%d"),
            "data": "AP01"
        }
        try:
            res = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=10, verify=False)
            res.raise_for_status()
            data = res.json()
            if isinstance(data, list) and data:
                base_data = data
                data_date = check_date
                # prev_data는 하루 전 데이터
                prev_date = check_date - datetime.timedelta(days=1)
                prev_data = requests.get(url, params={**params, "searchdate": prev_date.strftime("%Y%m%d")}, headers={"User-Agent": "Mozilla/5.0"}, timeout=10, verify=False).json()
                data_found = True
                break
        except Exception as e:
            print(f"⚠️ Failed to fetch data for {check_date}: {e}")

    if not data_found:
        return "💱[환율]\n⚠️ 최근 일주일 이내 환율 데이터를 불러올 수 없습니다."

    def extract_rate(data, unit):
        return next((float(i["deal_bas_r"].replace(',', '')) for i in data if i["cur_unit"] == unit), None)

    usd_base = extract_rate(base_data, "USD")
    usd_prev = extract_rate(prev_data, "USD")
    eur_base = extract_rate(base_data, "EUR")
    eur_prev = extract_rate(prev_data, "EUR")

    def diff_str(curr, prev):
        if curr is None or prev is None:
            return "-"
        diff = curr - prev
        emoji = "📈" if diff > 0 else ("📉" if diff < 0 else "")
        return f"{curr:,.2f} ({'+' if diff >= 0 else ''}{diff:.2f}) {emoji}"

    result = f"💱[환율] {data_date.strftime('%Y.%m.%d')} ({WEEKDAY_KO[data_date.weekday()]})"
    if now_kst.weekday() >= 5:
        result += " \n📢(주말 - 최신 데이터 표시)"
    result += f"\n💵USD: {diff_str(usd_base, usd_prev)}\n"
    result += f"💶EUR: {diff_str(eur_base, eur_prev)}"
    return result


def get_weather_dusseldorf(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "en"
    }

    def get_nearest_forecast(data, target_time):
        min_diff = datetime.timedelta(hours=1.5)
        nearest = None
        for item in data["list"]:
            dt = datetime.datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
            diff = abs(dt - target_time)
            if diff <= min_diff:
                min_diff = diff
                nearest = item
        return nearest

    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9)))
        result = ["🍺[날씨-Dusseldorf]"]
        offsets = [0, 6, 12, 24, 36, 48]
        forecast_times = [
            (now + datetime.timedelta(hours=offset)).replace(minute=0, second=0, microsecond=0)
            for offset in offsets
        ]

        for t in forecast_times:
            item = get_nearest_forecast(data, t)
            if item:
                temp = round(item["main"]["temp"])
                feels = round(item["main"]["feels_like"])
                desc = translate_weather(item["weather"][0]["description"])
                pressure = item["main"]["pressure"]
                humidity = item["main"]["humidity"]
                humidity_emoji = get_humidity_emoji(humidity)  # 습도 이모지 추가
                weekday_ko = WEEKDAY_EN_TO_KO[t.strftime("%a")]
                label = t.strftime(f"%m.%d ({weekday_ko}) %H:%M")
                emoji = get_temp_emoji(temp)  # 기온 이모지
                result.append(f"\n📅{label} : \n🌡️{temp}°C (체감 {feels}°C) {emoji}, {desc}, \n{pressure}hPa, \n습도 {humidity}% {humidity_emoji}")

        return "\n".join(result)
    except Exception as e:
        return f"Dusseldorf weather error: {e}"


def get_weather_seoul(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "en"
    }

    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9)))
        today = now.date()

        today_entries = [
            item for item in data["list"]
            if datetime.datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9))).date() == today
        ]

        if not today_entries:
            return "[Weather - Seoul]\nNo forecast data available for today."

        temps = [item["main"]["temp"] for item in today_entries]
        low = round(min(temps)) if temps else "-"
        high = round(max(temps)) if temps else "-"

        current_item = next(
            (item for item in today_entries
             if datetime.datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9))) > now),
            today_entries[0]
        )

        current = round(current_item["main"]["temp"])
        desc = translate_weather(current_item["weather"][0]["description"])
        emoji = get_temp_emoji(current)  # 기온 이모지
        humidity = current_item["main"]["humidity"]
        humidity_emoji = get_humidity_emoji(humidity)  # 습도 이모지 추가

        return f"🍚[날씨 - Seoul]\n🌡️현재: {current}°C {emoji}\n최저: {low}°C / 최고: {high}°C\n날씨: {desc}\n습도: {humidity}% {humidity_emoji}"
    except Exception as e:
        return f"Seoul weather error: {e}"



def send_kakao_message(access_token, friend_uuid, message_text):
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "receiver_uuids": json.dumps([friend_uuid]),
        "template_object": json.dumps({
            "object_type": "text",
            "text": message_text,
            "link": {
                "web_url": "https://www.kakao.com",
                "mobile_web_url": "https://www.kakao.com"
            }
        })
    }
    res = requests.post(url, headers=headers, data=data)
    print(res.status_code, res.text)

# Main execution
now_kst = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9)))
now_berlin = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Berlin"))
date_header = now_berlin.strftime("❗(독일): %Y.%m.%d (%a) %H:%M %Z\n")
date_header = date_header.replace(
    now_berlin.strftime("%a"), WEEKDAY_KO[now_berlin.weekday()]
)

access_token = refresh_access_token()
if not access_token:
    print("Failed to refresh token")
    exit()

message = date_header
message += get_exchange_rate() + "\n\n"
message += get_weather_dusseldorf(51.2277, 6.7735) + "\n\n"
message += get_weather_seoul(37.5665, 126.9780)

send_kakao_message(access_token, FRIEND_UUID, message)

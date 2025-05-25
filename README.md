# 🌦️ Kakao_Weather_Exchange_API_Bot

카카오 API, OpenWeather API, 한국수출입은행 환율 API를 연동하여 매일 **날씨 및 환율 정보를 자동 수집하고 카카오톡으로 알림 전송하는 Python 프로젝트**입니다.

---

## 📋 프로젝트 개요
- 🌐 **OpenWeather API**: 독일 뒤셀도르프 및 서울 날씨 예보 (최대 48시간)
- 💱 **한국수출입은행 환율 API**: USD, EUR 환율 정보 및 변화량
- 📢 **카카오 디벨로퍼 API**: 친구에게 카카오톡 메시지 전송
- 🔐 **.env 파일을 통한 API Key 및 민감정보 보안 관리** (업로드 X)
- ⏰ 매일 정해진 시간에 실행 가능 (예: 스케줄러 연동)

---

## 🛠️ 사용 기술 및 라이브러리
- **Python**: requests, json, dotenv, datetime, urllib3
- **API 연동**: OpenWeather, Kakao Developer, 한국수출입은행 API
- **환경변수 관리**: dotenv (.env 파일) (업로드 X)
- **카카오톡 전송**: KakaoTalk Friend Message API

---

## 🔑 주요 기능
- 독일(뒤셀도르프)와 서울의 기온, 체감온도, 습도, 기압 등 날씨 정보 제공
- USD, EUR 환율 및 전일 대비 변화량 계산 및 표시
- 카카오톡으로 메시지 전송 (알림용)
- 환경변수를 활용한 보안 유지 (업로드 X)
- 예외 처리 및 데이터 파싱 로직 포함

---
## 📂 파일 구조
┣ 📄 kakao_weather.py # 메인 실행 스크립트 (API 연동 및 메시지 전송)


---

## 🚀 향후 발전 방향
- Power BI, Tableau 연동으로 시각화 대시보드 구축
- 주간/월간 자동 보고서 생성 및 알림
- 사용자 지정 알림 및 실시간 알림 기능 강화

---

🔗 [포트폴리오 메인으로 돌아가기](https://github.com/jisuseo/Portfolio)


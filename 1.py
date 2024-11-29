
import asyncio
from telegram import Bot

async def main():
    access_token = ""  # API 토큰 입력
    bot = Bot(token=access_token)

    # 비동기적으로 업데이트 가져오기
    updates = await bot.get_updates()

    if updates:  # 업데이트가 있는지 확인
        chat_id = 
        #print(chat_id)

        # 메시지 보내기 (await 필수)
        await bot.send_message(chat_id=chat_id, text="안녕")
    else:
        print("새로운 업데이트가 없습니다.")

# 비동기 함수 실행
asyncio.run(main())


import telegram

access_token = ' ' # 본인의 텔레그램 봇 액세스 토큰
bot = telegram.Bot(token=access_token)
chat_id = bot.get_updates()[-1]. message.chat_id

bot.sendMessage(chat_id=chat_id, text = '안녕')
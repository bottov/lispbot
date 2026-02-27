#!venv/bin/python

import os
from telethon.sync import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def get_repl(code):
    code = code.replace('\n', '')
    code = code.replace('\\', '\\\\')
    code = code.replace('"', '\\"')
    print(code)
    res = os.popen(f'clisp -on-error exit -x "{code}" 2>&1')
    text = res.read()
    res.close()
    return text[840:-33]

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await bot.send_message(event.chat_id, 'Привет! Я бот-интерпретатор языка Лисп 🙂 Напишите валидный код и я верну результат 🫡')

@bot.on(events.NewMessage())
async def acho_all(event):
    if event.text == '/start': return
    text = get_repl(event.text)
    await bot.send_message(event.chat_id, text)

if __name__ == '__main__':
    bot.run_until_disconnected()

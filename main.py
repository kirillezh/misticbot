#import telethon
from telethon import TelegramClient, events
from telethon.tl.types import Message
#import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_media import *
from aiogram.types import ContentType

import logging, random
from array import *

from src.locales import API_ID, API_HASH, CHAT_ID, CHANNEL, API_TOKEN, SIREN, END, localisation

logging.basicConfig(format='[%(levelname) 5s] %(name)s: %(message)s', level=logging.INFO)

# Start telethon
client = TelegramClient('session',API_ID, API_HASH)
client.start()

# Start aiogram
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

from src.function import Function
from src.telegramAPI import telegramAPI
function = Function(bot)
botAPI = telegramAPI(bot)

#Siren
@client.on(events.NewMessage(chats=[CHANNEL]))
async def siren(message):
    await botAPI.sendReaction(CHAT_ID, 'upload_photo')
    if SIREN in str(message.message):
        caption = random.sample(localisation['ptn_xuilo'], k=1)[0]
    elif(END in str(message.message)):
        caption = localisation['vidboy']
    await botAPI.sendPhoto(CHAT_ID, function.screenshot(), caption)

#Send a screenshot
@dp.message_handler(commands=['screenshot'])
async def screenshot(message: types.Message):
    await botAPI.sendReaction(message.chat.id, 'upload_photo')
    await botAPI.sendPhoto(CHAT_ID, function.screenshot(), localisation['screenshot'], message.message_id)

#Start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await botAPI.reply(message, localisation['start'])

#Alert
@dp.message_handler(commands=['alert'])
async def alert(message: types.Message):
    await botAPI.reply(message, localisation['alert'])

#Info 
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await botAPI.reply(message, open("info.json", "r").read(), end="")

#Message distribution center
@dp.message_handler(content_types=types.ContentType.ANY)
async def mdc_all(message: types.Message):
    try:
        await function.logs(message)
        if(message.content_type in [ContentType.NEW_CHAT_MEMBERS]):
            await botAPI.reply(message, localisation['youbot1']+", "+message.new_chat_members[0].mention+". "+localisation['youbot2']+"!")
        if(message.content_type in [ContentType.LEFT_CHAT_MEMBER]):
            await botAPI.reply(message, localisation['leave'])
        if(message.content_type in [types.ContentType.VOICE, types.ContentType.VIDEO_NOTE]):
            await function.voicy2text(message)
        if(message.content_type in [types.ContentType.TEXT]):
            await function.tiktoktovideo(message)
            await function.youtubetovideo(message)
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)
#Start bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
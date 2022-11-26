#import telethon
from telethon import TelegramClient, events
from telethon.tl.types import Message
#import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_media import *
from aiogram.types import ContentType, Message

import logging, random
from array import *

from example import API_ID, API_HASH, CHAT_ID, CHANNEL, API_TOKEN, SIREN, END, localisation

from function import Function
function = Function()

# Start telethon
client = TelegramClient('progress',API_ID, API_HASH)
client.start()

# Start aiogram
bot = Bot(token=API_TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

#Siren
@client.on(events.NewMessage(chats=(CHANNEL)))
async def trevoga(message):
    await bot.send_chat_action(CHAT_ID, 'upload_photo')
    if(SIREN in str(message.message)):
        photo = open(function.screenshot(), 'rb')
        await bot.send_photo(
            chat_id=CHAT_ID, 
            photo=photo, 
            caption=f"{random.sample(localisation['ptn_xuilo'], k=1)[0]} \n{localisation['end']}", 
            parse_mode="HTML")
    elif(END in str(message.message)):
        photo = open(function.screenshot(), 'rb')
        await bot.send_photo(
            chat_id=CHAT_ID, 
            photo=photo, 
            caption=f"{localisation['vidboy']}\n{localisation['end']}", 
            parse_mode="HTML")

#Send a screenshot
@dp.message_handler(commands=['screenshot'])
async def screenshot(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'upload_photo')

    await bot.send_photo(
        chat_id=message.chat.id , 
        photo=open(function.screenshot(), 'rb'), 
        caption=f"{localisation['screenshot']}\n{localisation['end']}", 
        reply_to_message_id=message.message_id, 
        parse_mode="HTML")

#Start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await message.reply(
        f"{localisation['start']} \n{localisation['end']}",
        parse_mode="HTML", 
        disable_web_page_preview=True)

#Info bot
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    with open("info.json", "r") as file:
        lines =file.readlines()
        text = ''
        for line in lines:
            text += line
        await message.reply(
            text, 
            disable_web_page_preview=True)
#Welcome to the new member
@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await bot.send_message(
        message.chat.id, 
        f"{localisation['youbot1']}, {message.new_chat_members[0].mention}. {localisation['youbot2']}\n{localisation['end']}!",
        parse_mode="HTML", 
        disable_web_page_preview=True,
        reply_to_message_id=message.message_id)
#Missing a former member
@dp.message_handler(content_types=[ContentType.LEFT_CHAT_MEMBER])
async def left_members_handler(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await bot.send_message(
        message.chat.id, 
        f"{localisation['leave']}\n{localisation['end']}",
        parse_mode="HTML", 
        disable_web_page_preview=True,
        reply_to_message_id=message.message_id)

#Message distribution center
@dp.message_handler(content_types=types.ContentType.ANY)
async def mdc_all(message: types.Message):    
    try:
        await function.logs(message)
        await function.tiktoktovideo(bot, message)
        await function.youtubetovideo(bot, message)
        if(message.content_type in [types.ContentType.VOICE, types.ContentType.VIDEO_NOTE]):
            await function.voicy2text(bot, message)
    except:
        pass
#Start bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
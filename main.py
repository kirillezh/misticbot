#import telethon
from time import sleep
from telethon import TelegramClient, events
from telethon.tl.types import Message

#import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_media import *
from aiogram.types import ContentType, Message

import logging, random
from array import *

from example import API_ID, API_HASH, CHAT_ID, NOBOT, CHANNEL, API_TOKEN, sticker_id_pox, poebat_, trevog_i, otboi_i, close_i, livni_i, suka, sticker_id, name, otboi, testing_inform, master_xuilo, end, help, exit_

from function import check_mat, checker_tiktok, screenshot, hw

#start telethon
client = TelegramClient('progress',API_ID, API_HASH)
client.start()

#start aiogram
bot = Bot(token=API_TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

#TREVOGA
@client.on(events.NewMessage(chats=(CHANNEL)))
async def trevoga(message):
    await bot.send_chat_action(CHAT_ID, 'upload_photo')
    if(trevog_i in str(message.message)):
        photo = open(screenshot(), 'rb')
        await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=random.sample(master_xuilo, k=1)[0]+end, parse_mode="HTML")
    elif(otboi_i in str(message.message)):
        screenshot()
        photo = open(screenshot(), 'rb')
        await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=otboi+end, parse_mode="HTML")

#Help
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await message.reply(help,parse_mode="HTML", disable_web_page_preview=True)

#Похуй
@dp.message_handler(commands=['poxui'])
async def pox(message: types.Message):   
    mes = random.sample(sticker_id_pox, k=1)[0]
    try:
        if(message.reply_to_message.from_user.id!=NOBOT):
            if(random.randint(1,5)==1):
                await bot.send_chat_action(message.chat.id, 'record_voice')
                sleep(2)
                await bot.send_voice(chat_id=message.chat.id, voice=open('1.ogg', 'rb'),  caption=end, parse_mode="HTML")                
            else:
                await bot.send_chat_action(message.chat.id, 'choose_sticker')
                await message.reply_to_message.answer_sticker(mes, reply=message.reply_to_message)
        else:
            await message.answer("Ты кринж "+end, parse_mode="HTML", disable_web_page_preview=True)
    except:
        if(random.randint(1,5)==1):
            await bot.send_chat_action(message.chat.id, 'record_voice')
            await bot.send_voice(chat_id=message.chat.id, voice=open('1.ogg', 'rb'),  caption=end, parse_mode="HTML")                
        else:
            await bot.send_chat_action(message.chat.id, 'choose_sticker')
            await message.answer_sticker(mes)

#Поебать
@dp.message_handler(commands=['poebat'])
async def poebat(message: types.Message):   
    await bot.send_chat_action(message.chat.id, 'typing')
    try:
        if(message.reply_to_message.from_user.id!=NOBOT):
            await message.reply_to_message.answer(poebat_+end, reply=message.reply_to_message, parse_mode="HTML", disable_web_page_preview=True)
        else:
            await message.answer("Ты кринж "+end, parse_mode="HTML", disable_web_page_preview=True)
    except:
        await message.answer(poebat_ + end, parse_mode="HTML", disable_web_page_preview=True)
#Ливни
@dp.message_handler(commands=['livni'])
async def livni(message: types.Message):   
    await bot.send_chat_action(message.chat.id, 'typing')
    mes = livni_i+end
    try:
        if(message.reply_to_message.from_user.id!=NOBOT):
            await message.reply_to_message.answer(mes, reply=message.reply_to_message, parse_mode="HTML", disable_web_page_preview=True)
        else:
            await message.answer("Ты кринж "+end, parse_mode="HTML", disable_web_page_preview=True)
    except:
        await message.answer(mes, parse_mode="HTML", disable_web_page_preview=True)
        

#Cheerful check on the bot
@dp.message_handler(commands=['bot', 'Кто бот?'])
async def botik(message: types.Message):   
    await bot.send_chat_action(message.chat.id, 'typing')
    await message.reply(random.choices(name, weights=(3,4,2,1,1), k=1)[0]+" бот"+end, parse_mode="HTML", disable_web_page_preview=True)

#Stand with Ukraine * Fuck putin!
@dp.message_handler(commands=['putin', 'Кто путин?'])
async def xuilo(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await message.reply(random.sample(master_xuilo, k=1)[0]+end, parse_mode="HTML", disable_web_page_preview=True)

#HANDLE
@dp.message_handler(commands=['kerilhuesos', 'Ответ'])
async def reply(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await message.reply("Сам хуесос!"+end, parse_mode="HTML", disable_web_page_preview=True)

#Info
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    with open("info.json", "r") as file:
        lines =file.readlines()
        text = ''
        for line in lines:
            text += line
        await message.reply(text, disable_web_page_preview=True)

#GIF
@dp.message_handler(commands=['animal', 'gif'])
async def gif(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'choose_sticker')
    await message.answer_sticker(random.choices(sticker_id, k=1)[0], reply=message.message_id)
# Shut up
@dp.message_handler(commands=['close', 'Закрыть тему'])
async def close(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await message.reply(random.sample(close_i, k=1)[0]+' '+end, parse_mode="HTML", disable_web_page_preview=True)

#SCREENSHOT(ONLY TO @ezh_off)
@dp.message_handler(commands=['screenshot', 'Скриншот'])
async def screen(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'upload_photo')
    if(message.from_user.id != NOBOT):
        await message.reply(suka+end, parse_mode="HTML", disable_web_page_preview=True)
    else:
        photo = open(screenshot(), 'rb')
        await bot.send_photo(chat_id=message.chat.id , photo=photo, caption=testing_inform+" "+end, reply_to_message_id=message.message_id, parse_mode="HTML")

#AMC(All Message Checker)
@dp.message_handler()
async def AMC(message: types.Message):    
    await check_mat(message)
    await checker_tiktok(bot, message)
    await hw(bot)

@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    new_member = message.new_chat_members[0]
    await bot.send_message(message.chat.id, f"Привет, {new_member.mention}. Ты бот!")


@dp.message_handler(content_types=[ContentType.LEFT_CHAT_MEMBER])
async def new_members_handler(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await bot.send_message(message.chat.id, exit_)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
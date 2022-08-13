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

from example import API_ID, API_HASH, CHAT_ID, NOBOT, CHANNEL, API_TOKEN, TREVOGA, OTBOY, localisation

from function import Function

#start telethon
client = TelegramClient('progress',API_ID, API_HASH)
client.start()

#start aiogram
bot = Bot(token=API_TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

#Trevoga
@client.on(events.NewMessage(chats=(CHANNEL)))
async def trevoga(message):
    await bot.send_chat_action(CHAT_ID, 'upload_photo')
    if(TREVOGA in str(message.message)):
        photo = open(Function().screenshot(), 'rb')
        await bot.send_photo(
            chat_id=CHAT_ID, 
            photo=photo, 
            caption=f"{random.sample(localisation['ptn_xuilo'], k=1)[0]} \n{localisation['end']}", 
            parse_mode="HTML")
    elif(OTBOY in str(message.message)):
        photo = open(Function().screenshot(), 'rb')
        await bot.send_photo(
            chat_id=CHAT_ID, 
            photo=photo, 
            caption=f"{localisation['otboy']}\n{localisation['end']}", 
            parse_mode="HTML")

#Help
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await message.reply(
        f"{localisation['start']} \n{localisation['end']}",
        parse_mode="HTML", 
        disable_web_page_preview=True)

#Poxui
@dp.message_handler(commands=['poxui'])
async def pox(message: types.Message):   
    mes = random.sample(localisation['sticker_pox'], k=1)[0]
    try:
        if(message.reply_to_message.from_user.id!=NOBOT):
            if(random.randint(1,5)==1):
                await bot.send_chat_action(
                    message.chat.id, 
                    'record_voice')
                sleep(2)
                await bot.send_voice(
                    chat_id=message.chat.id, 
                    voice=open('1.ogg', 'rb'),  
                    caption=localisation['end'], 
                    parse_mode="HTML")                
            else:
                await bot.send_chat_action(
                    message.chat.id, 
                    'choose_sticker')
                await message.reply_to_message.answer_sticker(
                    mes, 
                    reply=message.reply_to_message)
        else:
            await message.answer(
                f"Ты кринж {localisation['end']}", 
                parse_mode="HTML", 
                disable_web_page_preview=True)
    except:
        if(random.randint(1,5)==1):
            await bot.send_chat_action(
                message.chat.id, 
                'record_voice')
            await bot.send_voice(
                chat_id=message.chat.id, 
                voice=open('1.ogg', 'rb'),  
                caption=localisation['end'], 
                parse_mode="HTML")                
        else:
            await bot.send_chat_action(
                message.chat.id, 
                'choose_sticker')
            await message.answer_sticker(mes)

#Поебать
@dp.message_handler(commands=['poebat'])
async def poebat(message: types.Message):   
    await bot.send_chat_action(message.chat.id, 'typing')
    try:
        if(message.reply_to_message.from_user.id!=NOBOT):
            await message.reply_to_message.answer(
                f"{localisation['poebat']}\n{localisation['end']}", 
                reply=message.reply_to_message, 
                parse_mode="HTML", 
                disable_web_page_preview=True)
        else:
            await message.answer(
                f"{localisation['youcringe']} \n {localisation['end']}", 
                parse_mode="HTML",
                disable_web_page_preview=True)
    except:
        await message.answer(
            f"{localisation['poebat']} \n{localisation['end']}", 
            parse_mode="HTML", 
            disable_web_page_preview=True)
#Ливни
@dp.message_handler(commands=['livni'])
async def livni(message: types.Message):   
    await bot.send_chat_action(message.chat.id, 'typing')
    try:
        if(message.reply_to_message.from_user.id!=NOBOT):
            await message.reply_to_message.answer(
                f"{localisation['livni']}\n{localisation['end']}", 
                reply=message.reply_to_message, 
                parse_mode="HTML", 
                disable_web_page_preview=True)
        else:
            await message.answer(
                f"{localisation['youcringe']} \n {localisation['end']}",
                parse_mode="HTML", 
                disable_web_page_preview=True)
    except:
        await message.answer(
            f"{localisation['livni']}\n{localisation['end']}", 
            parse_mode="HTML", 
            disable_web_page_preview=True)
        

#Cheerful check on the bot
@dp.message_handler(commands=['bot', 'Кто бот?'])
async def botik(message: types.Message):   
    await bot.send_chat_action(
        message.chat.id, 
        'typing')
    await message.reply(
        f"{random.choices(localisation['name'], weights=(3,4,2,1,1), k=1)[0]} {localisation['w_bot']} \n{localisation['end']}", 
        parse_mode="HTML", 
        disable_web_page_preview=True)

#Stand with Ukraine * Fuck putin!
@dp.message_handler(commands=['putin', 'Кто путин?'])
async def xuilo(message: types.Message):
    await bot.send_chat_action(
        message.chat.id, 
        'typing')
    await message.reply(
        f"{random.sample(localisation['ptn_xuilo'], k=1)[0]} \n{localisation['end']}", 
        parse_mode="HTML", 
        disable_web_page_preview=True)

#HANDLE
@dp.message_handler(commands=['kerilhuesos', 'Ответ'])
async def reply(message: types.Message):
    await bot.send_chat_action(
        message.chat.id, 
        'typing')
    await message.reply(
        f"{localisation['youxuesos']} \n{localisation['end']}", 
        parse_mode="HTML", 
        disable_web_page_preview=True)

#Info
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

#GIF
@dp.message_handler(commands=['animal', 'gif'])
async def gif(message: types.Message):
    await bot.send_chat_action(
        message.chat.id, 
        'choose_sticker')
    await message.answer_sticker(
        random.choices(localisation['sticker_animal'], k=1)[0], 
        reply=message.message_id)
#CAT
@dp.message_handler(commands=['cat', 'Cat'])
async def gif(message: types.Message):
    await bot.send_chat_action(
        message.chat.id, 
        'choose_sticker')
    await message.answer_sticker(
        random.choices(localisation['sticker_cat'], k=1)[0], 
        reply=message.message_id)

# Shut up
@dp.message_handler(commands=['close', 'Закрыть тему'])
async def close(message: types.Message):
    await bot.send_chat_action(
        message.chat.id, 
        'typing')
    await message.reply(
        f"{random.sample(localisation['close_topic'], k=1)[0]}\n{localisation['end']}", 
        parse_mode="HTML", 
        disable_web_page_preview=True)

#SCREENSHOT(ONLY TO @ezh_off)
@dp.message_handler(commands=['screenshot', 'Скриншот'])
async def screen(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'upload_photo')
    if(message.from_user.id != NOBOT):
        await message.reply(
            f"{localisation['inx']} \n{localisation['end']}", 
            parse_mode="HTML", 
            disable_web_page_preview=True)
    else:
        photo = open(Function().screenshot(), 'rb')
        await bot.send_photo(
            chat_id=message.chat.id , 
            photo=photo, 
            caption=f"{localisation['testtrevog']}\n{localisation['end']}", 
            reply_to_message_id=message.message_id, 
            parse_mode="HTML")

#AMC(All Message Checker)
@dp.message_handler()
async def AMC(message: types.Message):    
    await Function().check_mat(message)
    await Function().checker_tiktok(bot, message)
    await Function().HappyBirthday(bot)
    await Function().case_answwer(message)

@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    await bot.send_chat_action(
        message.chat.id, 
        'typing')
    new_member = message.new_chat_members[0]
    await bot.send_message(
        message.chat.id, 
        f"{localisation['youbot1']}, {new_member.mention}. {localisation['youbot2']}!",
        parse_mode="HTML", 
        disable_web_page_preview=True)


@dp.message_handler(content_types=[ContentType.LEFT_CHAT_MEMBER])
async def new_members_handler(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await bot.send_message(
        message.chat.id, 
        f"{localisation['leave']}\n{localisation['end']}",
        parse_mode="HTML", 
        disable_web_page_preview=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
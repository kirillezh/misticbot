#import telethon
from telethon import TelegramClient, events
#import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_media import *
from aiogram.types import ContentType, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

import logging, random
from array import *

from src.locales import API_ID, API_HASH, CHAT_ID, CHANNEL, API_TOKEN, localisation, cities, LEVELLOGGINING

logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(name)s: %(message)s', level=LEVELLOGGINING)

# Start telethon
client = TelegramClient('session',API_ID, API_HASH)
client.start()

# Start aiogram
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

from src.function import Function
from src.telegramAPI import telegramAPI
from src.session_pickle import SessionHelper

from src.dbHelper import dbHelper

botAPI = telegramAPI(bot)
session = SessionHelper()

database = dbHelper()

function = Function(bot, database)
#Siren
@client.on(events.NewMessage(chats=[CHANNEL]))
async def siren(message):
    row = await function.updateSiren(str(message.message))
    if(row != 'ok'):
        logging.warning(row)
    if(not session.read_data()['siren']):
        await function.sendSiren()

#Send a screenshot
@dp.message_handler(commands=['screenshot'])
async def screenshot(message: types.Message):
    try:
        row = database.full_check(message)
        if(row != 'ok'):
            logging.warning(row)
        group = database.infoGroup(message.chat.id)
        await function.screenshotSend(message.chat.id, localisation[group[5]]['screenshot'], message.message_id)
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)

#Start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        row = database.full_check(message)
        if(row != 'ok'):
            logging.warning(row)
        group = database.infoGroup(message.chat.id)
        await botAPI.reply(message, localisation[group[5]]['start'], lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)


#Settings
def mainSettingsButtons(group: int):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=(localisation[group[5]]['settings']['main']['setLang']+": "+localisation[group[5]]['name']), callback_data="listLang"))
    keyboard.add(types.InlineKeyboardButton(text=(localisation[group[5]]['settings']['main']['setAccess']+": "+localisation[group[5]]['settings']['role'][group[4]]), callback_data="listAccess"))
    keyboard.add(types.InlineKeyboardButton(text=(('🔴️️', '🟢')[group[6] == 1]+localisation[group[5]]['settings']['main']['set_Alert']), callback_data="set_Alert"))
    if(group[0] < 0 and group[6] == 1):
        keyboard.add(types.InlineKeyboardButton(text=(localisation[group[5]]['settings']['main']['setCity']), callback_data="listCity"))
    keyboard.add(types.InlineKeyboardButton(text=(('🔴️️', '🟢')[group[9] == 1]+localisation[group[5]]['settings']['main']['set_Voicy']), callback_data="set_Voicy"))
    keyboard.add(types.InlineKeyboardButton(text=(('🔴️️', '🟢')[group[10] == 1]+localisation[group[5]]['settings']['main']['set_TikTok']), callback_data="set_TikTok"))
    keyboard.add(types.InlineKeyboardButton(text=(('🔴️️', '🟢')[group[11] == 1]+localisation[group[5]]['settings']['main']['set_Youtube']), callback_data="set_Youtube"))
    keyboard.add(types.InlineKeyboardButton(text=(('🔴️️', '🟢')[group[12] == 1]+localisation[group[5]]['settings']['main']['set_Reels']), callback_data="set_Reels"))
    keyboard.add(types.InlineKeyboardButton(text=(('🔴️️', '🟢')[group[13] == 1]+localisation[group[5]]['settings']['main']['set_Twitter']), callback_data="set_Twitter"))
    keyboard.add(types.InlineKeyboardButton(text=(localisation[group[5]]['settings']['main']['exit']), callback_data="set_Exit"))
    return keyboard

def languageSettingsButtons(group: int):
    keyboard = types.InlineKeyboardMarkup()
    for lang in localisation:
        keyboard.add(types.InlineKeyboardButton(text=(('', '🟢')[group[5] == lang]+localisation[lang]['name']), callback_data=("setLang_"+lang)))
    keyboard.add(types.InlineKeyboardButton(text=(localisation[group[5]]['settings']['main']['toMain']), callback_data=("toMain")))
    return keyboard

def citiesSettingsButtons(group: int):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for city in cities:
        keyboard.insert(types.InlineKeyboardButton(text=(('', '🟢')[group[7] == cities[city]]+city), callback_data=("setCity_"+cities[city])))
    keyboard.add(types.InlineKeyboardButton(text=(localisation[group[5]]['settings']['main']['toMain']), callback_data=("toMain")))
    return keyboard

def accessLevelSettingsButtons(group: int):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for level in localisation[group[5]]['settings']['role']:
        keyboard.add(types.InlineKeyboardButton(text=(('', '🟢')[group[4] == level]+localisation[group[5]]['settings']['role'][level]), callback_data=("setLevel_"+level)))
    keyboard.add(types.InlineKeyboardButton(text=(localisation[group[5]]['settings']['main']['toMain']), callback_data=("toMain")))
    return keyboard


@dp.message_handler(commands=['settings'])
async def settings(message: types.Message):
    try:
        row = database.full_check(message)
        if(row != 'ok'):
            logging.warning(row)
        group = database.infoGroup(message.chat.id)

        level = await function.checkStatus(message.from_user.id, message.chat.id)
        if(not level):
            return await botAPI.reply(message,localisation[group[5]]['settings']['error']['level'] ,lang=group[5])
        
        await botAPI.replyWithButtons(message, localisation[group[5]]['settings']['main']['text'], keyboard=mainSettingsButtons(group), lang=group[5], end="", reply=False)
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)

@dp.callback_query_handler(text="toMain")
async def toMain(call: types.CallbackQuery):
    try:
        group = database.infoGroup(call.message.chat.id)
        
        level = await function.checkStatus(call.from_user.id, call.message.chat.id)
        if(not level):
            return await call.answer(localisation[group[5]]['settings']['error']['level'], show_alert=True)

        await botAPI.editTextWithButtons(call.message, localisation[group[5]]['settings']['main']['text'], keyboard=mainSettingsButtons(group), lang=group[5], end="")
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)


@dp.callback_query_handler(text="listLang")
async def listLang(call: types.CallbackQuery):
    try:
        group = database.infoGroup(call.message.chat.id)

        level = await function.checkStatus(call.from_user.id, call.message.chat.id)
        if(not level):
            return await call.answer(localisation[group[5]]['settings']['error']['level'], show_alert=True)

        await botAPI.editTextWithButtons(call.message, localisation[group[5]]['settings']['main']['text']+': '+localisation[group[5]]['settings']['main']['setLang'], languageSettingsButtons(group), end='', lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)

@dp.callback_query_handler(Text(startswith="setLang_"))
async def setLang(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    try:
        group = database.infoGroup(call.message.chat.id)

        level = await function.checkStatus(call.from_user.id, call.message.chat.id)
        if(not level):
            return await call.answer(localisation[group[5]]['settings']['error']['level'], show_alert=True)

        if(lang == group[5]):
            return
        row = database.updateGroup(call.message.chat.id, 'group_lang', str(lang))
        if(row !='ok'):
            logging.warning(row)
            return
        group = database.infoGroup(call.message.chat.id)
        await botAPI.editTextWithButtons(call.message, localisation[group[5]]['settings']['main']['text']+': '+localisation[group[5]]['settings']['main']['setLang'], languageSettingsButtons(group), end='', lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)


@dp.callback_query_handler(text="listCity")
async def listCity(call: types.CallbackQuery):
    try:
        group = database.infoGroup(call.message.chat.id)

        level = await function.checkStatus(call.from_user.id, call.message.chat.id)
        if(not level):
            return await call.answer(localisation[group[5]]['settings']['error']['level'], show_alert=True)

        if(group[0] > 0):
            return await call.answer(localisation[group[5]]['settings']['error']['personal'], show_alert=True)

        await botAPI.editTextWithButtons(call.message, localisation[group[5]]['settings']['main']['text']+': '+localisation[group[5]]['settings']['main']['setCity'], citiesSettingsButtons(group), end='', lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)

@dp.callback_query_handler(Text(startswith="setCity_"))
async def setCity(call: types.CallbackQuery):
    city = call.data.split("_")[1]
    try:
        group = database.infoGroup(call.message.chat.id)

        level = await function.checkStatus(call.from_user.id, call.message.chat.id)
        if(not level):
            return await call.answer(localisation[group[5]]['settings']['error']['level'], show_alert=True)
        
        if(group[0] > 0):
            return await call.answer(localisation[group[5]]['settings']['error']['personal'], show_alert=True)
        if(city == group[7]):
            return
        row = database.updateGroup(call.message.chat.id, 'group_city', str(city))
        if(row !='ok'):
            logging.warning(row)
            return
        group = database.infoGroup(call.message.chat.id)
        await botAPI.editTextWithButtons(call.message, localisation[group[5]]['settings']['main']['text']+': '+localisation[group[5]]['settings']['main']['setCity'], citiesSettingsButtons(group), end='', lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)


@dp.callback_query_handler(text="listAccess")
async def listAccess(call: types.CallbackQuery):
    try:
        group = database.infoGroup(call.message.chat.id)

        level = await function.checkStatus(call.from_user.id, call.message.chat.id)
        if(not level):
            return await call.answer(localisation[group[5]]['settings']['error']['level'], show_alert=True)

        if(group[0] > 0):
            return await call.answer(localisation[group[5]]['settings']['error']['personal'], show_alert=True)

        await botAPI.editTextWithButtons(call.message, localisation[group[5]]['settings']['main']['text']+': '+localisation[group[5]]['settings']['main']['setAccess'], accessLevelSettingsButtons(group), end='', lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)

@dp.callback_query_handler(Text(startswith="setLevel_"))
async def setLevel(call: types.CallbackQuery):
    levelTo = call.data.split("_")[1]
    try:
        group = database.infoGroup(call.message.chat.id)

        level = await function.checkStatus(call.from_user.id, call.message.chat.id)
        if(not level):
            return await call.answer(localisation[group[5]]['settings']['error']['level'], show_alert=True)

        if(group[0] > 0):
            return await call.answer(localisation[group[5]]['settings']['error']['personal'], show_alert=True)
        if(levelTo == group[4]):
            return
        row = database.updateGroup(call.message.chat.id, 'group_admins', str(levelTo))
        if(row !='ok'):
            logging.warning(row)
            return
        group = database.infoGroup(call.message.chat.id)
        await botAPI.editTextWithButtons(call.message, localisation[group[5]]['settings']['main']['text']+': '+localisation[group[5]]['settings']['main']['setAccess'], accessLevelSettingsButtons(group), end='', lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)


@dp.callback_query_handler(Text(startswith="set_"))
async def setSettings(call: types.CallbackQuery):
    action = call.data.split("_")[1]
    try:
        group = database.infoGroup(call.message.chat.id)

        level = await function.checkStatus(call.from_user.id, call.message.chat.id)
        if(not level):
            return await call.answer(localisation[group[5]]['settings']['error']['level'], show_alert=True)

        if(action=='Alert'):
            action = 'group_siren'
            arg = 6
            if(group[0] > 0):
                return await call.answer(localisation[group[5]]['settings']['error']['personal'], show_alert=True)
        elif(action=='Voicy'):
            action = 'group_voicy'
            arg = 9
        elif(action=='TikTok'):
            action = 'group_tiktok'
            arg = 10
        elif(action=='Youtube'):
            action = 'group_youtube'
            arg = 11
        elif(action=='Reels'):
            action = 'group_reels'
            arg = 12
        elif(action=='Twitter'):
            action = 'group_twitter'
            arg = 13
        elif(action=='Exit'):
            return await botAPI.editText(call.message, localisation[group[5]]['settings']['main']['final'], lang=group[5])
        else:
            return
        row = database.updateGroup(call.message.chat.id, action, (1, 0)[group[arg] == 1])
        if(row !='ok'):
            logging.warning(row)
            return
        group = database.infoGroup(call.message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        await botAPI.editTextWithButtons(call.message, localisation[group[5]]['settings']['main']['text'], mainSettingsButtons(group) , end='', lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)

#Alert
@dp.message_handler(commands=['alert'])
async def alert(message: types.Message):
    try:
        row = database.full_check(message)
        if(row != 'ok'):
            logging.warning(row)
        group = database.infoGroup(message.chat.id)
        await botAPI.reply(message, localisation[group[5]]['alert'], lang=group[5])
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)

#Info 
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    try:
        row = database.full_check(message)
        if(row != 'ok'):
            logging.warning(row)
        group = database.infoGroup(message.chat.id)
        await botAPI.reply(message, localisation[group[5]]['version']+': '+function.checkLocalInfo('version'), end="")
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)

#Message distribution center
@dp.message_handler(content_types=types.ContentType.ANY)
async def mdc_all(message: types.Message):
    try:
        row = database.full_check(message)
        if(row != 'ok'):
            logging.warning(row)
        group = database.infoGroup(message.chat.id)
        
        if(message.content_type in [ContentType.NEW_CHAT_MEMBERS]):
            if(not message.new_chat_members[0].is_bot):
                await botAPI.reply(message, localisation[group[5]]['youbot1']+", "+message.new_chat_members[0].mention+". "+localisation[group[5]]['youbot2']+"!")
            else:
                me = await botAPI.me()
                if(message.new_chat_members[0].id == me.id):
                    await botAPI.reply(message, localisation[group[5]]['start'], lang=group[5])

        if(message.content_type in [ContentType.LEFT_CHAT_MEMBER]):
            if(not message.left_chat_member.is_bot):
                await botAPI.reply(message, localisation[group[5]]['leave'])
            else:
                me = await botAPI.me()
                if(message.left_chat_member.id == me.id):
                    row = database.updateGroup(group[0], 'group_siren', False)
                    if(row != 'ok'):
                        logging.warning(row)
        if(group[9] == 1):
            if(message.content_type in [types.ContentType.VOICE, types.ContentType.VIDEO_NOTE]):
                await function.voicy2text(message)
        if(message.content_type in [types.ContentType.TEXT]):
            if(group[10] == 1):
                await function.tiktoktovideo(message)
            if(group[11] == 1):
                await function.youtubetovideo(message)
            if(group[12] == 1):
                await function.instatovideo(message)
            if(group[13] == 1):
                await function.twittertovideo(message)
            
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)
#Start bot
async def on_startup(call):
    await function.on_startup()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    

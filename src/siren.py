from src.locales import DRIVER, GMT, localisation, cities, API_TOKEN_ALERT, defenitionAPIUID
import logging, json, os
from src.telegramAPI import telegramAPI
from src.APIScreenshot import APIScreenshot
from src.dbHelper import dbHelper

import asyncio
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from io import BytesIO

class Siren:
    def __init__(self, bot, database, function):
        logger_ = logging.getLogger("logger")
        logger_.setLevel(logging.ERROR)
        self.screenshotAPI = APIScreenshot()
        self.botAPI = telegramAPI(bot)
        self.database = database
        self.function = function
        self.alert_client = AsyncAlertsClient(token=API_TOKEN_ALERT)

    def formatSiren(self, listSiren: list) -> list:
        updatelist = []
        for uid, nameUkr in listSiren:
                nameEng = defenitionAPIUID[uid]
                updatelist.append((uid, nameEng))
        return updatelist

    async def getSirenAPI(self) -> (list, BytesIO):
        try:
            air_raid_locations = await self.alert_client.get_active_alerts()
        except:
            raise Exception("API Reach Limit. You should call API no more than 3-4 times per minute")
        locations = air_raid_locations.filter('alert_type', "air_raid", 'location_type', "oblast")
        sirenList = []
        for alert in locations:
            sirenList.append((alert.location_uid, alert.location_title))
        return self.formatSiren(sirenList)

    def compareSiren(self, nowAPIList: list, dbAPI: list) -> (list, list):
        siren = [item[1] for item in nowAPIList]
        allClear = []
        for iD, name, status in dbAPI:
            if((not name in siren) and status == 1):
                allClear.append(name)
        return (siren, allClear)

    #Start Function 
    async def startSiren(self):
        while(True):
            try:
                nowSirenList = await self.getSirenAPI()
            except Exception as e:
                logging.warning(e)
                await asyncio.sleep(60)
                continue

            dbSirenList = self.database.allCity()
            sirenList, allClearList = self.compareSiren(nowSirenList, dbSirenList)
            for city in sirenList:
                row = self.database.updateCity(city, 1)
                if(row != 'ok'):
                    logging.error('DB_ERROR', row)

            for city in allClearList:
                row = self.database.updateCity(city, 0)
                if(row != 'ok'):
                    logging.error('DB_ERROR', row)
                await self.allClear(city)

            await self.sendSiren()
            await asyncio.sleep(13)
        await self.startSiren()

    #Function to check group where need to send message about status Siren
    async def checkGroupSiren(self):
        cities = self.database.allCity()
        groupWithSiren = []
        for city in cities:
            if city[2] == 1:
                groups = self.database.groupWithCity(city[1])
                if(groups != []):
                    for group in groups:
                        if(group[6] == 1):
                            groupWithSiren.append(group)
        return groupWithSiren
    #Send Air siren all clear
    async def allClear(self, city: str):
        theme = self.function.timeTheme()
        groups = self.database.groupWithCity(city)
        if(groups == []):
            return
        iDS = []
        for group in groups:
            row = self.database.updateGroup(group[0], 'group_siren_id', '')
            if(row != 'ok'):
                logging.error('DB_ERROR', row)
            try:
                msg = await self.function.sendPhotoFromSeesion(group[0], 'clean'+theme, (localisation[group[5]]['vidboy']))
                iDS.append((msg, group[5]))
            except Exception as e:
                logging.warning('Error at %s', 'division', exc_info=e)
            try:
                if(group[8] != ''):
                        await self.botAPI.unpinMessage(group[0], group[8])
            except:
                pass
        screenshot = await self.screenshotAPI.screenshot_alert()
        for mes, lang in iDS:
            try:
                await self.botAPI.editPhoto(mes, screenshot, (localisation[lang]['vidboy']), lang=lang)
            except:
                pass
    #Function to send siren-messages to chats
    async def sendSiren(self):
        theme = self.function.timeTheme()
        groups = await self.checkGroupSiren()
        if(groups == []):
            return
        for group in groups:
            if(group[8] in ['',None]):
                try:
                    msg = await self.function.sendPhotoFromSeesion(group[0], 'siren'+theme, localisation[group[5]]['sirenMessage'] + ' ' + ((group[7]+(' Region','')[group[7] in ['Kyiv Region', 'Kyiv city', 'Autonomous Republic of Crimea']]), self.function.get_key(cities, group[7]))[group[5] == 'ua'] + "\n"+localisation[group[5]]['map_siren'])
                    row = self.database.updateGroup(group[0], 'group_siren_id', msg.message_id)
                    if(row != 'ok'):
                        return row
                except Exception as e:
                    logging.warning('Error at %s', 'division', exc_info=e)
        try:
            screenshot = await self.screenshotAPI.screenshot_alert()
        except:
            pass
        for group in groups:
            if(not group[8] in ['',None]):
                try:
                    await self.botAPI.editPhotoByIds(group[0], group[8], screenshot, localisation[group[5]]['sirenMessage'] + ' ' + ((group[7]+(' Region','')[group[7] in ['Kyiv Region', 'Kyiv city', 'Autonomous Republic of Crimea']]), self.function.get_key(cities, group[7]))[group[5] == 'ua'] + "\n"+localisation[group[5]]['map_siren'])
                except:
                    pass    
        import os
        try:
            os.remove('screenshot.png')
        except:
            pass

    #Send now screenshot map
    async def screenshotSend(self, chatID: int, caption:str, message_id: int = None):
        theme = self.function.timeTheme()
        try:
            msg = await self.function.sendPhotoFromSeesion(chatID, 'loadMaps'+theme,caption, message_id)
        except:
            msg = await self.function.sendPhotoFromSeesion(chatID, 'loadMaps'+theme,caption)
        try:
            msg_new = await self.botAPI.editPhoto(msg, await self.screenshotAPI.screenshot_alert('screenshot_temp.png'), caption)
        except:
            msg_new = await self.function.updatePhotoFromSeesion(message = msg,photoid= 'error'+theme,caption = caption)
        import os
        try:
            os.remove('screenshot_temp.png')
        except:
            pass
        return msg_new
from src.locales import DRIVER, GMT, localisation, cities, SIREN, ENDSIREN
import logging, json
from src.telegramAPI import telegramAPI
from src.twitterAPI import twitterAPI
from src.session_pickle import SessionHelper
from src.APIScreenshot import APIScreenshot
from src.tiktokAPI import snaptik
from src.dbHelper import dbHelper

class loggerYT(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Function:
    def __init__(self, bot, database):
        self.screenshotAPI = APIScreenshot()
        self.botAPI = telegramAPI(bot)
        self.twitter = twitterAPI()
        logger_ = logging.getLogger("logger")
        logger_.setLevel(logging.ERROR)
        self.session = SessionHelper()
        self.database = database

    def checkLocalInfo(self, var):
        f = json.load(open('info.json'))
        return f[var]

    async def on_startup(self):
        dbVersion = self.database.infoBot()[2]
        version = self.checkLocalInfo('version')
        versionTo = self.checkLocalInfo('upgrade')

        if(float(dbVersion) < float(version)):
            self.database.updateInfoBot(version)
            if(float(dbVersion) < float(versionTo['versionTo'])):
                groups = self.database.allGroup()
                for group in groups:
                    try:
                        await self.botAPI.sendMessage(group[0], versionTo['updateInfo'][group[5]], lang=group[5], end="")
                    except Exception as e:
                        logging.warning('Error at %s', 'division', exc_info=e)
        
    async def checkStatus(self, userID: int, groupID: int):
        try:
            statusUser = await self.botAPI.getChatMember(userID, groupID)
        except Exception as e:
            logging.warning('Error at %s', 'division', exc_info=e)
            return False
        statusGroup = self.database.infoGroup(groupID)[4]
        if(statusGroup == 'member' or statusUser == 'creator'):
            return True
        if(statusUser == statusGroup):
            return True
        
        return False
        
    async def checkSiren(self, text: str):
        siren = False
        if(SIREN in text):
            siren = True
        elif(ENDSIREN in text):
            siren = False
        else:
            return False
        name = ""
        for city in cities:
            if(city in text):
                return {
                    "status":siren,
                    "city": cities[city] 
                }
        return False

    async def updateSiren(self, text: str):
        siren = await self.checkSiren(text)
        row = self.database.updateCity(siren['city'], siren['status'])
        if(row != 'ok'):
            return row
        if(siren['status'] == False):
            groups = self.database.groupWithCity(siren['city'])
            screenshot = await self.screenshotAPI.screenshot_alert()
            for group in groups:
                row = self.database.updateGroup(group[0], 'group_siren_id', '')
                if(row != 'ok'):
                    return row
                try:
                    msg = await self.sendSirenMessage(group[0], (localisation[group[5]]['vidboy']), False, False)
                    await self.botAPI.editPhoto(msg, screenshot, (localisation[group[5]]['vidboy']))
                    await self.botAPI.unpinMessage(group[0], group[8])
                except:
                    pass
        return 'ok'
        
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
    def get_key(self, d, value):
        for k, v in d.items():
            if v == value:
                return k
        return None

    async def sendSiren(self):
        groups = await self.checkGroupSiren()
        if(groups == []):
            self.session.update_somedata('siren', False)
            return 'ok'
        self.session.update_somedata('siren', True)
        try:
            screenshot = await self.screenshotAPI.screenshot_alert()
        except:
            pass
        for group in groups:
            if(group[8] in ['',None]):
                try:
                    msg = await self.sendSirenMessage(group[0], localisation[group[5]]['sirenMessage'] + ' ' + ((group[7]+(' Region','')[group[7] in ['Kyiv Region', 'Kyiv city', 'Autonomous Republic of Crimea']]), self.get_key(cities, group[7]))[group[5] == 'ua'] + "\n"+localisation[group[5]]['map_siren'] , True)
                    row = self.database.updateGroup(group[0], 'group_siren_id', msg.message_id)
                    if(row != 'ok'):
                        return row
                except Exception as e:
                    logging.warning('Error at %s', 'division', exc_info=e)
            else:
                try:
                    await self.botAPI.editPhotoByIds(group[0], group[8], screenshot, localisation[group[5]]['sirenMessage'] + ' ' + ((group[7]+(' Region','')[group[7] in ['Kyiv Region', 'Kyiv city', 'Autonomous Republic of Crimea']]), self.get_key(cities, group[7]))[group[5] == 'ua'] + "\n"+localisation[group[5]]['map_siren'])
                except:
                    pass    
        import os
        try:
            os.remove('screenshot.png')
        except:
            pass
        await self.sendSiren()

    async def sendPhotoFromSeesion(self, chatid: int, photoid : str, caption: str = "", messageId: str = None):
        photo = self.database.photo(photoid)
        if(photo == None):
            mes = await self.botAPI.sendPhoto(chatid,"src/media/"+photoid+".png", caption, messageId)
            row = self.database.newPhoto(self.idMaxPhoto(mes), photoid)
            if(row != 'ok'):
                logging.critical(row)
        else:
            try:
                mes = await self.botAPI.sendPhotobyID(chatid,photo, caption, messageId)
            except:
                mes = await self.botAPI.sendPhoto(chatid,"src/media/"+photoid+".png", caption, messageId)
                row = self.database.newPhoto(self.idMaxPhoto(mes), photoid)
                if(row != 'ok'):
                    logging.critical(row)
        return mes
    
    async def updatePhotoFromSeesion(self, message, photoid : str, caption: str = ""):
        photo = self.database.photo(photoid)[0]
        if(photo == None):
            mes = await self.botAPI.editPhoto(message,"src/media/"+photoid+".png", caption)
            row = self.database.newPhoto(self.idMaxPhoto(mes), photoid)
            if(row != 'ok'):
                logging.critical(row)
        else:
            try:
                mes = await self.botAPI.editPhotobyID(message,photo, caption)
            except:
                mes = await self.botAPI.editPhoto(message,"src/media/"+photoid+".png", caption)
                row = self.database.newPhoto(self.idMaxPhoto(mes), photoid)
                if(row != 'ok'):
                    logging.critical(row)
        return 
    
    def idMaxPhoto(self,message):
        photo_sizes = message.photo
        photo_sizes.sort(key=lambda photo_size: photo_size.width, reverse=True)
        photo_id = photo_sizes[0].file_id
        return photo_id

    async def sendSirenMessage(self, chatid, caption: str, siren: bool, pinned: bool = True):
        import datetime, asyncio
        time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
        if time_h in range(8, 22):
            theme = 'Light'
        else:
            theme = 'Dark'
        if siren:
            photoId= 'siren'+theme
        else:
            photoId= 'clean'+theme
        msg = await self.sendPhotoFromSeesion(
                    chatid=chatid,
                    photoid= photoId,
                    caption = caption
                )
        if pinned:
            try:
                await self.botAPI.pinMessage(chatid, msg.message_id)
            except:
                pass
        
        return msg

    async def screenshotSend(self, chatID: int, caption:str, message_id: int = None):
        import datetime
        time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
        if time_h in range(7, 20):
            theme = 'Light'
        else:
            theme = 'Dark'
        try:
            msg = await self.sendPhotoFromSeesion(chatID, 'loadMaps'+theme,caption, message_id)
        except:
            msg = await self.sendPhotoFromSeesion(chatID, 'loadMaps'+theme,caption)
        await self.botAPI.sendReaction(chatID, 'upload_photo')
        try:
            msg_new = await self.botAPI.editPhoto(msg, await self.screenshotAPI.screenshot_alert(), caption)
        except:
            msg_new = await self.updatePhotoFromSeesion(message = msg,photoid= 'error'+theme,caption = caption)
        import os
        try:
            os.remove('screenshot.png')
        except:
            pass
        return msg_new
    

    #voicy2text
    async def voicy2text(self, message):
        group = self.database.infoGroup(message.chat.id)
        import os
        from src.convert import Converter
        msg = await self.botAPI.reply(message, localisation[group[5]]['load_v2t'])
        file_id = message.voice.file_id if message.content_type in ['voice'] else message.video_note.file_id
        file_info = await self.botAPI.getFile(file_id)
        file_name = str(message.message_id) + '.ogg'
        await self.botAPI.downloadFile(file_info.file_path, file_name)
        converter = Converter(file_name)
        os.remove(file_name)
        message_text = converter.audio_to_text()
        del converter
        if(message_text == None):
            return await self.botAPI.editText(msg, localisation[group[5]]['fail_v2t'])
        return await self.botAPI.editText(msg, message_text)

    #search url from text
    def searchurl(self, text):
        split_text = text.split()
        for i in split_text:
            if "http" in i:
                link = i
        try:
            return link
        except:
            return ''


    #checking and sending tiktok-video
    async def tiktoktovideo(self, message):
        url=self.searchurl(message.text)
        if("vm.tiktok.com/" in url):
            import datetime
            time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
            if time_h in range(8, 22):
                theme = 'Light'
            else:
                theme = 'Dark'
            try:
                msg = await self.sendPhotoFromSeesion(
                    chatid=message.chat.id,
                    photoid= 'load'+theme,
                    messageId = message.message_id
                )
                await self.botAPI.sendReaction(message.chat.id, 'upload_video')
                video_data = await snaptik(url)
                if video_data == None:
                    await self.updatePhotoFromSeesion(
                        message = msg,
                        photoid= 'error'+theme
                    )
                else:
                    await self.botAPI.editVideo(
                    message= msg,
                    videoId = video_data["link"], 
                    text= video_data["name"])
            except Exception as e:
                await self.updatePhotoFromSeesion(
                        message = msg,
                        photoid= 'error'+theme
                    )
                logging.warning('Error at %s', 'division', exc_info=e)
            


    #checking and sending youtube-video
    async def youtubetovideo(self, message):
        url=self.searchurl(message.text)
        if("youtube.com/" in url or "youtu.be/" in url):
            await self.botAPI.sendReaction(message.chat.id, 'upload_video')
            file = self.youtubeapi(url)
            try:
                if(file != None):
                    await self.botAPI.sendVideoURL(
                        toСhat = message.chat.id, 
                        videoURL = file["link"], 
                        messageId = message.message_id,
                        caption = file["name"])
            except Exception as e:
                logging.warning('Error at %s', 'division', exc_info=e)
                

    #url video
    def youtubeapi(self, text):
        from yt_dlp import YoutubeDL
        ydl_opts = {'logger':loggerYT()}
        yt = YoutubeDL(ydl_opts)
        r = yt.extract_info(text, download=False)
        try:
            urls = [f for f in r['formats'] if f['video_ext'] == 'mp4' and f['acodec'] != 'none' and f['vcodec'] != 'none' and f['filesize_approx'] < 20900000]         
        except KeyError as e:
            urls = [f for f in r['formats'] if f['video_ext'] == 'mp4' and f['acodec'] != 'none' and f['vcodec'] != 'none' and ( (f['filesize'] != None and f['filesize'] < 20900000))]
        if(urls == []):
            return None
        try:
                vid = {
                    "link": urls[0]['url'],
                    "name": r['title']
                }
                return vid
        except:
                return None

    #checking and sending insta-video
    async def instatovideo(self, message):
        url=self.searchurl(message.text)
        if("instagram.com/reel/" in url):
            import datetime
            time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
            if time_h in range(8, 22):
                theme = 'Light'
            else:
                theme = 'Dark'
            
            try:
                msg = await self.sendPhotoFromSeesion(
                    chatid=message.chat.id,
                    photoid= 'load'+theme,
                    messageId = message.message_id
                )
                await self.botAPI.sendReaction(message.chat.id, 'upload_video')
                info = self.instaAPI(url=url)
                await self.botAPI.editVideo(
                    message= msg,
                    videoId = info["link"], 
                    text= info["name"])
            except Exception as e:
                await self.updatePhotoFromSeesion(
                        message = msg,
                        photoid= 'error'+theme
                    )
                logging.warning('Error at %s', 'division', exc_info=e)
    
    #search video from url
    def instaAPI(self, url):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.common.keys import Keys
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument('--disable-dev-shm-usage')
        #chrome_options.add_argument('User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"')
        driver = webdriver.Chrome(executable_path=DRIVER,options=chrome_options)
        driver.get("https://saveinsta.app/en1")
        urlField = driver.find_element_by_id("s_input")
        urlField.send_keys(url)
        urlField.send_keys(Keys.ENTER)
        try:
            vid = {
                "link": WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/div/div/div[3]/ul/li[1]/div/div[2]/a').get_attribute('href')),
                "name": ""
            }
        except:
            vid = ""
            pass
        driver.quit()
        return vid

    #checking and sending twitter-video
    async def twittertovideo(self, message):
        url=self.searchurl(message.text)
        if("twitter.com/" in url):
            import datetime
            time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
            if time_h in range(8, 22):
                theme = 'Light'
            else:
                theme = 'Dark'
            
            try:
                msg = await self.sendPhotoFromSeesion(
                    chatid=message.chat.id,
                    photoid= 'load'+theme,
                    messageId = message.message_id
                )
                await self.botAPI.sendReaction(message.chat.id, 'upload_video')
                info = self.twitter.getvideo(url)
                await self.botAPI.editVideo(
                    message= msg,
                    videoId = info["link"], 
                    text= info["name"])
            except Exception as e:
                await self.updatePhotoFromSeesion(
                        message = msg,
                        photoid= 'error'+theme
                    )
                logging.warning('Error at %s', 'division', exc_info=e)
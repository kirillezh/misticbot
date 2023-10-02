from src.locales import DRIVER, GMT, localisation, cities
import logging, json, os
from src.telegramAPI import telegramAPI
from src.twitterAPI import twitterAPI
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
        self.botAPI = telegramAPI(bot)
        self.twitter = twitterAPI()
        logger_ = logging.getLogger("logger")
        logger_.setLevel(logging.ERROR)
        self.database = database

    def checkLocalInfo(self, var):
        f = json.load(open('info.json'))
        return f[var]

    def get_key(self, d, value):
        for k, v in d.items():
            if v == value:
                return k
        return None

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
                        if(versionTo['photo'] != ''):
                            await self.botAPI.sendPhoto(toСhat=group[0], photoId=('src/media/'+versionTo['photo']+self.timeTheme()+'.png'), caption=versionTo['updateInfo'][group[5]], lang=group[5], end="")
                        else:
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
        

    async def sendPhotoFromSeesion(self, chatid: int, photoid : str, caption: str = "", messageId: str = None):
        photo = self.database.photo(photoid)
        if(photo is None):
            mes = await self.botAPI.sendPhoto(chatid,"src/media/"+photoid+".png", caption, messageId)
            row = self.database.newPhoto(self.idMaxPhoto(mes), photoid)
            if(row != 'ok'):
                logging.critical(row)
        else:
            try:
                mes = await self.botAPI.sendPhotobyID(chatid,photo[0], caption, messageId)
            except:
                mes = await self.botAPI.sendPhoto(chatid,"src/media/"+photoid+".png", caption, messageId)
                row = self.database.newPhoto(self.idMaxPhoto(mes), photoid)
                if(row != 'ok'):
                    logging.critical(row)
        return mes
    
    async def updatePhotoFromSeesion(self, message, photoid : str, caption: str = ""):
        photo = self.database.photo(photoid)
        if(photo is None):
            mes = await self.botAPI.editPhoto(message,"src/media/"+photoid+".png", caption)
            row = self.database.newPhoto(self.idMaxPhoto(mes), photoid)
            if(row != 'ok'):
                logging.critical(row)
        else:
            try:
                mes = await self.botAPI.editPhotobyID(message,photo[0], caption)
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
    def timeTheme(self):
        import datetime
        time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')

        return 'Light' if time_h in range(8, 22) else 'Dark'

    #checking and sending tiktok-video
    async def tiktoktovideo(self, message):
        url=self.searchurl(message.text)
        if("vm.tiktok.com/" in url):
            try:
                msg = await self.sendPhotoFromSeesion(
                    chatid=message.chat.id,
                    photoid= 'load'+self.timeTheme(),
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
                        photoid= 'error'+self.timeTheme()
                    )
                logging.warning('Error at %s', 'division', exc_info=e)
            


    #checking and sending youtube-video
    async def youtubetovideo(self, message):
        url = self.searchurl(message.text)
        group = self.database.infoGroup(message.chat.id)
        if("youtube.com/" in url or "youtu.be/" in url):
            msg = await self.sendPhotoFromSeesion(
                    chatid=message.chat.id,
                    photoid= 'load'+self.timeTheme(),
                    messageId = message.message_id
                )
            await self.botAPI.sendReaction(message.chat.id, 'upload_video')
            idVideo, titleVideo = self.youtubeapiID(url)
            video = self.database.photo(f'youtube_{idVideo}')
            if(not video is None):
                await self.botAPI.editVideo(msg, video[0], titleVideo, lang=group[5])
            else:
                try:
                    file = self.youtubeapi(url)
                    msg = await self.botAPI.editVideoFile(message = msg, destVideo = 'video/'+file, text=titleVideo, lang=group[5])
                    self.database.newPhoto(msg.video.file_id, 'youtube_'+idVideo)
                except Exception as e:
                    await self.updatePhotoFromSeesion(
                        message = msg,
                        photoid= 'error'+self.timeTheme()
                    )
                    logging.warning('Error at %s', 'division', exc_info=e)
                os.remove('video/'+file)

    def format_selector(self, ctx):
        formats = ctx.get('formats')[::-1]
        best_video = next(f for f in formats
                        if f['vcodec'] != 'none' and f['acodec'] == 'none' and (f['quality'] in range(7,9)) and f['ext'] != 'webm')
        audio_ext = {'mp4': 'm4a'}[best_video['ext']]
        best_audio = next(f for f in formats if (
            f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))
        yield {
            'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
            'ext': best_video['ext'],
            'requested_formats': [best_video, best_audio],
            'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
        }

    def youtubeapiID(self, url):
        from yt_dlp import YoutubeDL
        ydl_opts = {'logger':loggerYT()}
        ydl = YoutubeDL(ydl_opts)
        info = ydl.extract_info(url, download=False)
        return info['id'], info['title']

    #url video
    def youtubeapi(self, url):
        from yt_dlp import YoutubeDL
        ydl_opts = {
            'format': self.format_selector,
            'outtmpl': os.path.join('video', '%(id)s.%(ext)s'),
            'logger':loggerYT()
        }

        ydl = YoutubeDL(ydl_opts)
        info = ydl.extract_info(url, download=True)
        inf = list(self.format_selector(info))[0]
        return info['id'] + '.' + inf['ext']


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
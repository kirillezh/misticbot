from src.locales import DRIVER, GMT, URL, localisation, TIKTOKUSE
import logging 
from src.telegramAPI import telegramAPI
from src.session_pickle import SessionHelper
#from instagrapi import Client, exceptions
class loggerYT(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Function:
    def __init__(self, bot):
        self.botAPI = telegramAPI(bot)
        logger_ = logging.getLogger("logger")
        logger_.setLevel(logging.ERROR)
        self.session = SessionHelper()
    
    async def sendPhotoFromSeesion(self, chatid: int, photoid : str, caption: str = "", messageId: str = None):
        photo =  self.session.read_photo(photoid)
        if(photo == ''):
            mes = await self.botAPI.sendPhoto(chatid,"src/media/"+photoid+".png", caption, messageId)
            self.session.update_photo(photoid, self.idMaxPhoto(mes))
        else:
            try:
                mes = await self.botAPI.sendPhotobyID(chatid,photo, caption, messageId)
            except:
                mes = await self.botAPI.sendPhoto(chatid,"src/media/"+photoid+".png", caption, messageId)
                self.session.update_photo(photoid, self.idMaxPhoto(mes))
        return mes
    
    async def updatePhotoFromSeesion(self, message, photoid : str, caption: str = ""):
        photo =  self.session.read_photo(photoid)
        if(photo == ''):
            mes = await self.botAPI.editPhoto(message,"src/media/"+photoid+".png", caption)
            self.session.update_photo(photoid, self.idMaxPhoto(mes))
        else:
            try:
                mes = await self.botAPI.editPhotobyID(message,photo, caption)
            except:
                mes = await self.botAPI.editPhoto(message,"src/media/"+photoid+".png", caption)
                self.session.update_photo(photoid, self.idMaxPhoto(mes))
        return 
    
    def idMaxPhoto(self,message):
        photo_sizes = message.photo
        photo_sizes.sort(key=lambda photo_size: photo_size.width, reverse=True)
        photo_id = photo_sizes[0].file_id
        return photo_id
    
    async def screenshotSendSiren(self, chatid, caption: str, pinned: bool = True):
        import datetime, asyncio
        time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
        if time_h in range(8, 22):
            theme = 'light'
        else:
            theme = 'dark'
        msg = await self.botAPI.sendPhotobyID(chatid, localisation['img'][theme], caption)
        if pinned:
            await self.botAPI.pinMessage(chatid, msg.message_id)
        while True:
            try:
                await self.botAPI.editPhoto(msg, await self.screenshot(), caption)
            except:
                pass
            data = self.session.read_data()
            if data['siren'] is False:
                if pinned:
                    await self.botAPI.unpinMessage(chatid, msg.message_id)
                return 0
            await asyncio.sleep(8)


    async def screenshotSend(self, chatID: int, caption:str, message_id: int = None):
        import datetime
        time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
        if time_h in range(8, 22):
            theme = 'Light'
        else:
            theme = 'Dark'
        try:
            msg = await self.sendPhotoFromSeesion(chatID, 'loadMaps'+theme,caption, message_id)
        except:
            msg = await self.sendPhotoFromSeesion(chatID, 'loadMaps'+theme,caption)
        await self.botAPI.sendReaction(chatID, 'upload_photo')
        try:
            return await self.botAPI.editPhoto(msg, await self.screenshot(), caption)
        except:
            return await self.updatePhotoFromSeesion(
                        message = msg,
                        photoid= 'error'+theme,
                        caption = caption
                    )
    

    #voicy2text
    async def voicy2text(self, message):
        import os
        from src.convert import Converter
        msg = await self.botAPI.reply(message, localisation['load_v2t'])
        file_id = message.voice.file_id if message.content_type in ['voice'] else message.video_note.file_id
        file_info = await self.botAPI.getFile(file_id)
        file_name = str(message.message_id) + '.ogg'
        await self.botAPI.downloadFile(file_info.file_path, file_name)
        converter = Converter(file_name)
        os.remove(file_name)
        message_text = converter.audio_to_text()
        del converter
        if(message_text == None):
            return await self.botAPI.editText(msg, localisation['fail_v2t'])
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
                video_data = self.tiktokAPI(url)
                if video_data=="" :
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
                logging.warning('Error at %s', 'division', exc_info=e)
            

    #search video from url
    def tiktokAPI(self, url):
        if(TIKTOKUSE == "False"):
            return self.tiktokAPIaletrnative(url=url)
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=DRIVER,options=chrome_options)
        driver.get(url)
        try:
            vid = {
                "link": WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div/video').get_attribute('href')),
                "name": WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div').text)
            }
        except:
            vid = self.tiktokAPIaletrnative(url=url)
        driver.quit()
        return vid
    
    #search video from url
    def tiktokAPIaletrnative(self, url):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.common.keys import Keys
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=DRIVER,options=chrome_options)
        driver.get("https://snaptik.app/en")
        urlField = driver.find_element_by_id("url")
        urlField.send_keys(url)
        urlField.send_keys(Keys.ENTER)
        try:
            vid = {
                "link": WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(by=By.XPATH, value='/html/body/section/div/div[2]/div/div[2]/a[1]').get_attribute('href')),
                "name": WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(by=By.XPATH, value='/html/body/section/div/div[2]/div/div[1]/div/div').text)
            }
            if(vid['name'] == "No description"):
                vid['name']=""
        except:
            vid = ""
            pass
        driver.quit()
        return vid

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

    async def screenshot(self):
        import asyncio, datetime
        from pyppeteer import launch
        time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
        if time_h in range(8, 22):
            theme = 'light'
        else:
            theme = 'black-preset'
        try:
            browser = await launch(defaultViewport={
                "width": 1600,
                "height": 1200,
                "isMobile": False,
                "hasTouch":False,
                "isLandscape":False
            }, logLevel = logging.WARNING, options={'args': ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--single-process', '--no-zygote']})
            page = await browser.newPage()
            await page.goto(URL)
            await page.evaluate("document.querySelector('html').className = '"+theme+" menu-hidden'")
            await asyncio.sleep(5)
            await page.screenshot({'path': 'screenshot.png'})
            await browser.close()
        except Exception as e:
                logging.warning('Error at %s', 'division', exc_info=e)
        return 'screenshot.png'

    #logs to file
    async def logs(self, message):
        import datetime
        file = open("logs.txt", "a")
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        file.write(f"{message.from_user.id}-{message.from_user.full_name}-{now}-{message}\n")
        file.close()

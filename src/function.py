from src.locales import DRIVER, GMT, URL, localisation
import logging 
from src.telegramAPI import telegramAPI
class Function:
    def __init__(self, bot):
        self.botAPI = telegramAPI(bot)
        
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
            await self.botAPI.sendReaction(message.chat.id, 'upload_video')
            video_data = self.tiktokAPI(url)
            try:
                await self.botAPI.sendVideoURL(
                    toСhat = message.chat.id, 
                    videoURL = video_data, 
                    messageId = message.message_id)
            except Exception as e:
                logging.warning('Error at %s', 'division', exc_info=e)
            

    #search video from url
    def tiktokAPI(self, url):
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
        video = dict()
        try:
            video = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.TAG_NAME, value='video').get_attribute('src'))
        except:
            video = self.tiktokAPIaletrnative(url=url)
        driver.quit()
        return video
    
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
            video = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(by=By.XPATH, value='/html/body/main/div[2]/div/div/div[2]/div/a[1]').get_attribute('href'))
        except:
            video = ""
            pass
        driver.quit()
        return video

    #checking and sending youtube-video
    async def youtubetovideo(self, message):
        url=self.searchurl(message.text)
        if("youtube.com/" in url or "youtu.be/" in url):
            await self.botAPI.sendReaction(message.chat.id, 'upload_video')
            file = self.youtubeapi(url)
            try:
                await self.botAPI.sendVideoURL(
                    toСhat = message.chat.id, 
                    videoURL = file["link"], 
                    messageId = message.message_id,
                    caption = file["name"])
            except Exception as e:
                logging.warning('Error at %s', 'division', exc_info=e)

    #url video
    def youtubeapi(self, text):
        from pytube import YouTube
        yt = YouTube(text)
        try:
            vid = {
                "link": yt.streams[1].url,
                "name": yt.title
            }
            return vid
        except:
            return 'error'

    #work with screenshot
    def screenshot(self):
        import datetime
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-setuid-sandbox")
        driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)
        driver.set_window_size(1680, 1200)
        driver.get(URL)
        time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
        if time_h in range(8, 22):
            theme = 'light'
        else:
            theme = 'dark'
        try:
            WebDriverWait(driver, timeout=10).until(lambda d: d.execute_script(f"arguments[0].setAttribute('class','{theme} menu-hidden')", driver.find_element(By.TAG_NAME, 'html')))
        except:
            pass
        driver.save_screenshot("screenshot.png")
        driver.quit()
        return 'screenshot.png'

    #logs to file
    async def logs(self, message):
        import datetime
        file = open("logs.txt", "a")
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        file.write(f"{message.from_user.id}-{message.from_user.full_name}-{now}-{message}\n")
        file.close()

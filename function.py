from example import DRIVER, GMT, URL, localisation

class Function:
    #voicy2text
    async def voicy2text(self, bot, message):
        msg = await message.answer(
            f"{localisation['load_v2t']}\n{localisation['end']}", 
            parse_mode="HTML", 
            disable_web_page_preview=True,
            reply=message.message_id)
        import os
        from convert import Converter
        file_id = message.voice.file_id if message.content_type in ['voice'] else message.video_note.file_id
        file_info = await bot.get_file(file_id)
        file_name = str(message.message_id) + '.ogg'
        await bot.download_file(file_info.file_path, file_name)
        converter = Converter(file_name)
        os.remove(file_name)
        message_text = converter.audio_to_text()
        del converter
        if(message_text == None):
            return await msg.edit_text(
            f"{localisation['fail_v2t']}\n{localisation['end']}",
            parse_mode="HTML", 
            disable_web_page_preview=True)
        return await msg.edit_text(
                f"{message_text}\n{localisation['end']}",
                parse_mode="HTML", 
                disable_web_page_preview=True)

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
    async def tiktoktovideo(self, bot, message):
        url=self.searchurl(message.text)
        if("vm.tiktok.com/" in url):
            await bot.send_chat_action(message.chat.id, 'upload_video')
            video_data=self.tiktokapi(url)
            try:
                await bot.send_video(
                    message.chat.id, 
                    video_data['url'], 
                    reply_to_message_id=message.message_id, 
                    caption=localisation['end'],
                    parse_mode="HTML")
            except:
                pass

    #search video from url
    def tiktokapi(self, url):
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
            video['url'] = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.TAG_NAME, value='video').get_attribute('src'))
        except:
            video['url'] = ''
        driver.quit()
        return video

    #checking and sending youtube-video
    async def youtubetovideo(self, bot, message):
        url=self.searchurl(message.text)
        if("youtube.com/" in url or "youtu.be/" in url):
            await bot.send_chat_action(message.chat.id, 'upload_video')
            file = self.youtubeapi(url)
            try:
                await bot.send_video(
                    message.chat.id, 
                    file["link"],
                    reply_to_message_id=message.message_id,
                    caption=file["name"])
            except:
                pass

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
        
        if(time_h>=22 or time_h<=8):
            try:
                WebDriverWait(driver, timeout=10).until(lambda d: d.execute_script("arguments[0].setAttribute('class','dark menu-hidden')", driver.find_element(By.TAG_NAME, 'html')))
            except:
                pass
        else:
            try:
                WebDriverWait(driver, timeout=10).until(lambda d: d.execute_script("arguments[0].setAttribute('class','light menu-hidden')", driver.find_element(By.TAG_NAME, 'html')))
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

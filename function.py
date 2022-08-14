#import selenium(chrome)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import datetime, random
from roughfilter import search_obscene_words
from time import sleep

from example import DRIVER, CHAT_ID, GMT, URL_TREVOG, NOBOT, localisation

from bd import DataBase

class Function:
    #happy birthday
    async def HappyBirthday(self, bot):   
        nowdate = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))).strftime('%d.%m.%Y')
        info = DataBase().find(nowdate)
        for i in info:
            DataBase().update(i[0])
            if(i[2]==None):
                await bot.send_message(CHAT_ID, f"{localisation['hb1']} \n{i[3]}, {localisation['hb2']}!) \n{localisation['end']}")
            else:
                await bot.send_message(CHAT_ID,f"{localisation['hb3']} \n<a href='tg://user?id={i[2]}'>{i[3]}</a>, {localisation['hb2']}! \n{localisation['end']}", parse_mode="HTML")

    #check mat in message    
    async def check_mat(self, message):
        mes=str(message.text)
        mes=mes.lower()
        try:
            ifcheck=search_obscene_words(str(message.text))
        except:
            ifcheck = False
        if(ifcheck and message.from_user.id != NOBOT):
                if('кирилл' in mes  or 'керил' in mes or 'кирил' in mes or 'крил' in mes or 'киирил' in mes):
                    await message.reply(f"{localisation['inx']} \n{localisation['end']}",parse_mode="HTML", disable_web_page_preview=True)
                elif(random.randint(1, 10000)==1):
                    await message.reply(f"{localisation['offmat']} \n{localisation['end']}",parse_mode="HTML", disable_web_page_preview=True)

    #checking and sending tiktok-video
    async def checker_tiktok(self, bot, message):
        url_light=self.text_to_url(message.text)
        if("tiktok.com/" in url_light):
            await bot.send_chat_action(message.chat.id, 'upload_video')
            video_data=self.url_to_video(url_light)
            try:
                await bot.send_video(message.chat.id, video_data['url'], reply_to_message_id=message.message_id, caption=localisation['end'],parse_mode="HTML")
            except:
                await message.reply(f"{localisation['bag']} \n{localisation['end']}", parse_mode="HTML", disable_web_page_preview=True)

    #work with screenshot
    def screenshot(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-setuid-sandbox")
        driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)
        driver.set_window_size(1680, 1200)
        driver.get(URL_TREVOG) 

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

    #search url from text
    def text_to_url(self, text):
        split_text = text.split()
        for i in split_text:
            if "http" in i:
                link = i
        try:
            return link
        except:
            return ''


    #search video from url
    def url_to_video(self, url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=DRIVER,options=chrome_options)
        driver.get(url) 
        video = dict()
        sleep(2)
        try:
            video['url'] = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div/div/video').get_attribute('src'))
        except:
            video['url'] = ''
        driver.quit()
        return video
    #answer 
    async def case_answwer(self, message):
        text = str(message.text)
        split_text = text.lower().split()
        for i in split_text:
            l = localisation['answer'].get(i, None)
            if(l != None):
                await message.reply_sticker(l)

    #logs to file
    async def logs(self, message):
        file = open("logs.txt", "a")
        file.write(f"{message.from_user.id} - {message.from_user.full_name}\n")
        file.close()

#import selenium(chrome)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import datetime, random
from roughfilter import search_obscene_words
from time import sleep

from example import DRIVER, FUCK_YOU, GMT, URL_TREVOG, OFFMAT, end, NOBOT

#check nomer in text

def to_sym(mes):
    s = []
    for t in mes.split():
        try:
            s.append(float(t))
        except ValueError:
            pass
    return s


#check mat in message    
async def check_mat(message):
    mes=str(message.text)
    mes=mes.lower()
    try:
        ifcheck=search_obscene_words(str(message.text))
    except:
        ifcheck = False
    if(ifcheck and message.from_user.id != NOBOT):
            if('кирилл' in mes  or 'керил' in mes or 'кирил' in mes or 'крил' in mes or 'киирил' in mes):
                await message.reply(FUCK_YOU+end,parse_mode="HTML", disable_web_page_preview=True)
            elif(random.randint(1, 10000)==1):
                await message.reply(OFFMAT+end,parse_mode="HTML", disable_web_page_preview=True)

#checking and sending tiktok-video
async def checker_tiktok(bot, message):
    
    url_light=text_to_url(message.text)
    if("tiktok.com/" in url_light):
        await bot.send_chat_action(message.chat.id, 'upload_video')
        video_data=url_to_video(url_light)
        try:
            await bot.send_video(message.chat.id, video_data['url'], reply_to_message_id=message.message_id, caption=end,parse_mode="HTML")
        except:
            await message.reply('Ошибка! Дам, это баг:(' + end, parse_mode="HTML", disable_web_page_preview=True)

#work with screenshot
def screenshot():
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
def text_to_url(text):
    split_text = text.split()
    for i in split_text:
        if "http" in i:
            link = i
    try:
        return link
    except:
        return ''


#search video from url
def url_to_video(url):
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

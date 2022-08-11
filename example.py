from aiogram.utils.markdown import hlink
import os
from dotenv import load_dotenv

#import .env file
load_dotenv()
NOBOT = int(os.getenv('NOBOT'))
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
CHAT_ID = int(os.getenv('CHAT_ID'))
API_TOKEN = os.getenv('API_TOKEN')
DRIVER = os.getenv('DRIVER')
CHANNEL = os.getenv('CHANNEL')
URL_TREVOG = os.getenv('URL_TREVOG')
GMT = int(os.getenv('GMT'))
TREVOGA = os.getenv('TREVOGA')
OTBOY = os.getenv('OTBOY')

localisation = {
    "fuck_you":"Не смей оскорблять Кирилла! Ебал я тебя!",
    "offmat":"Сука, не матерись, блять. Заебал тут материться, ебало щас снесу!",
    "otboy": "С отбоем хуя!",
    "livni":"Съебался с чата!",
    "poebat":"Поебать, так поебать",
    "inx":"Иди нахуй!",
    "hb1": "Сегодня День Варенья у кого-то...",
    "hb2": "с Днём Рождения",
    "hb3": "Оу.... Сегодня День Рождения у кого-то...",
    "bag": "Ошибка! Дам, это баг:(",
    "testtrevog":"чё за хуйня? а не, просто ТЕСТ!",
    "leave":"Эх... не выдержал токсичности группы и сбежал...",
    "end": "<a href='https://secure.wayforpay.com/payment/ukraine.army'>Stand with Ukraine 🇺🇦🇺🇦🇺🇦</a>",
    "youcringe": "Ты кринж",
    "youxuesos": "Сам хуесос!",
    "youbot1": "Привет",
    "youbot2": "Ты бот",
    "w_bot": "бот",
    "start": 'Hi, ёбта)) \n\nДа, я немного странный бот, но зато у меня есть много прикольных функций... \n\nНапример, я могу твои тики-токи с обычной ссылки в видосик переводить... Ну тебе ж лень скачать видео, правда?)\nМогу найти бота в чате, или хуйла-путина, также уведомляю и хуесошу, когда последний хочет запустить в Днепр ракету, также радуюсь когда отменяют тревогу\nЕсть ещё несколько функций... Но об них узнаете позже)\n\nВсем любви и мира, кроме русских❤️',
    "name": ['Егор','Даня', 'Гоша', 'Кирилл', 'Ягуб'],
    "ptn_xuilo": ['путин хуйло', 'Їбав я путіна у сраку!', 'путин пошёл нахуй!', 'Ебал я путина!', 'путин хуйло!', 'путин пидорас!', 'Нахуй путина!', 'Когда ж здохнет путин?!', 'путин пидор', 'путин сосёт у ВСУ', 'Как же этот лысик заебал...', 'Путин на аве, а мать...', 'Путина пора отправить в дурку', 'Покажіть вже путіну слідана, а то задовбав захищати'],
    "close_topic": ['Закрываем тему.', 'Close the topic.', ' Konu kapandi.', 'Закриваємо тему.', '關閉主題.', 'Позакривали пиздаки. У нас тут лояльний чат. \nтему закрито!', 'Пропоную мирне рішення, закриваємо тему та спатки!', 'club незадоволений. \nЗакриваємо тему, прийшов час для Anal Sex'],
    "sticker_pox": ['CAACAgIAAxkBAAEElDliakULZ3j-zpu67UHSbgH_RjxkJQACcg8AAqeYuEqeM4W80euEtiQE', 'CAACAgIAAxkBAAEElDdiakUISVluzt2A3wABIlWBY3WoWLsAAqsSAAJaTrFKpPnj6An5jhgkBA', 'CAACAgIAAxkBAAEElDViakUHzKl694RjvHVS8XAnZ7lYPAAC2RAAAt0OqErP2RLbp3ggCSQE', 'CAACAgIAAxkBAAEElDNiakUFYgOiUasAAdewh7ywGrtiLS0AAjQRAAIZUalKF7noQSFTzg4kBA', 'CAACAgIAAxkBAAEElDFiakTwhpu5tT2vYQ270Wh-XTELggAC-RAAAmFqoErkw0vII7zrCyQE', 'CAACAgIAAxkBAAEElC9iakTuS7tqPgt9MQERO7S9sdhYHwACihMAAp1oqErSb2wPGvkKrSQE', 'CAACAgIAAxkBAAEElC1iakTkDF336j_S9Fgs3IQWtKDqwAAC3A8AAsP0qErHaW8bq1ZWbiQE'],
    "sticker_animal": ['CAACAgIAAxkBAAEEdzJiV-0gRuQx_kHiY16HrFXskoOyhgACcBYAAkyguUkF5J_2PYzKAAEjBA', 'CAACAgIAAxkBAAEEdzRiV-0iWJShyS9HGcibdFky6xNkMQACbBgAAmsxsUnYO6GW9aWYsSME', 'CAACAgIAAxkBAAEEdzZiV-0ja1RUkeBjWzxkxbux9bz5bAACihUAAmTesUnEWlOzw3-pHyME', 'CAACAgIAAxkBAAEEdzhiV-0lR54_nk6Toa7WR8Ax9Ub1RQACoxoAAn3IsEnvBspucjqWsSME', 'CAACAgIAAxkBAAEEdzpiV-0pJ9m4JsJJMQfUmgABRFWKTLAAArMbAAINYLFJKd9uoJxOTNEjBA', 'CAACAgIAAxkBAAEEdzxiV-0r2XuIbrVi-X-SdMdbRgzv6wACXxYAAh0SuEkQH5yqfLtBDiME', 'CAACAgIAAxkBAAEEdz5iV-0t9nud8vO9ajvxUYsAASYazkYAAlsbAAIQeLFJNeB82OMPWXQjBA', 'CAACAgIAAxkBAAEEd0BiV-0vrPcmgm6ULR79KTLHy4KW0wACWBkAAr-usUl_Jc1ApjPtmSME', 'CAACAgIAAxkBAAEEd0JiV-0wH88dgteilVYdHpmgnRKjXgAC8RUAAoS_sUleJpom4YEwniME', 'CAACAgIAAxkBAAEEd0RiV-0zTdTq6eOC54y52ocDPOweuwACfBYAAj7RuEmGaIOvmkr4gyME', 'CAACAgIAAxkBAAEEd0ZiV-01UJ-JOggMZalyjtqWMKmmrQACjBQAAt99uEkaNy6pbj_glSME','CAACAgIAAxkBAAEEd0hiV-02Lk-a_IlFpQlCSM-MQG8WJQACNhUAAk7tuEk_cn2bQEqhPyME', 'CAACAgIAAxkBAAEEd0liV-04vLO9-GYupH1muMK7odqd6QACJxgAAuzGuUlYwcwnbjjQ1CME', 'CAACAgIAAxkBAAEEd0xiV-052N8n8gZbx5VqTvclgS0nmwACIBgAAs7VuEkq5q0RWKpJXyME', 'CAACAgIAAxkBAAEEd05iV-07udU1b3tveb7pPCWx0lbYXAACjBYAAgbauElaX6hTSYBPsiME', 'CAACAgIAAxkBAAEEd1BiV-088qM-wAK7sIE3S6_3GC0MpQACFBgAAntDuEn4p2jY8f9DwiME', 'CAACAgIAAxkBAAEEd1JiV-0-sQHylcgjIixSN0aRKF2ZjwAClRUAAj-CuUnAZYFEy3_RPSME', 'CAACAgIAAxkBAAEEd1RiV-1CCcmj4BieXW4Pn1FJgRZoCgACPRsAAtMu0UnUKelpd3QGRCME', 'CAACAgIAAxkBAAEEd1ViV-1Ep9WXyDRUjB5IW62jbjUjMAACuBkAAjWL0Ul71NGl4NviOiME', 'CAACAgIAAxkBAAEEiKZiYnsogPn557IAAc_ls0GGQl30jioAAn0UAAJB7gABS0QFepbyBe0mJAQ', 'CAACAgIAAxkBAAEEiKhiYnsqabodWvpY6z7TYdRF3xr1QgACrhkAAmEr-Uo9Rzj7nwcxayQE', 'CAACAgIAAxkBAAEEiKpiYnsrFE5qxV_HqNKUVGl2ZFL5qwAC8RUAAjq8AAFLYJpSRRQHdGokBA', 'CAACAgIAAxkBAAEEiKxiYnstfBatEgLQWIs_UNLmNfSV_wACVRQAAu9MAUuB-wOXn7tZqCQE', 'CAACAgIAAxkBAAEEiK5iYnsuMXVIHUVw-xG3rN41NYtIowACehoAAmSL-UptVF2mWpYtOiQE', 'CAACAgIAAxkBAAEEiLBiYnsxUZp8WzjNgo_md_0IIvzNlQACZxQAAuUQAUus1DvMCV3pxyQE', 'CAACAgIAAxkBAAEEiLJiYnsyou-n3v79S8o87zlh9kXcVgACjhUAAmJXEUu8o-3vtQVekiQE', 'CAACAgIAAxkBAAEEiLRiYnszDqEP8KFDbliOe4-4CK_I0wACPBUAAuKnEUsM1ieOZhp1OiQE'],
    "answer": {
        "кринж": 'CAACAgIAAxkBAAEFiVxi9TXrkJp2EzDBwp2ou7O6ZNUXOAACJh0AAr_tsEvR8FtbWLuOUSkE',
        "момент": 'CAACAgIAAxkBAAEFiV5i9TX2_izaid_O-6s5MKSAQdpefAACPxwAAjlxqUsypiYNE43PzykE'
    }
}
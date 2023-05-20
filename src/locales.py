import os
from dotenv import load_dotenv

#import .env file
load_dotenv()
INSTA_LOGIN = os.getenv('INSTA_LOGIN')
INSTA_PASS = os.getenv('INSTA_PASS')

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

CHAT_ID = int(os.getenv('CHAT_ID'))

API_TOKEN = os.getenv('API_TOKEN')

DRIVER = os.getenv('DRIVER')

CHANNEL = os.getenv('CHANNEL')

URL = os.getenv('URL')

GMT = int(os.getenv('GMT'))

SIREN = os.getenv('SIREN')
END = os.getenv('END')

RANDOM = os.getenv('RANDOM')

LEVELLOGGINING = str(os.getenv('LEVELLOGGINING'))

TIKTOKUSE = str(os.getenv('TIKTOKUSE'))

localisation = {
    "load_v2t": "зачекай... намагаюсь зрозуміти твою солов'їну",
    "fail_v2t": "Ні чорта не зрозумів🤬",
    "local_v2t":{
        "идинахуй": "иди нахуй😡",
        "Путин": "хуйло🤬",
        "Росси": "соси😡",
        "м****":"минет😡",
        "з*******":"заебался😡",
        "з******":"заебала😡",
        "з*****":"заебал😡",
        "д******": "дрочіла😡",
        "д****": "дохуя😡",
        "б****": "блядь😡",
        "ж***": "жопа(-ы)😡",
        "х****": "хуйло😡",
        "х**": "хуй😡",
        "с***": "сука😡",
        "н****": "нахуй😡",
        "п******": "підорас😡",
        "п*****": "піздец😡",
        "п****": "пізда😡",
        "е*******":"ебальник",
        "б**":"бля",
        "е****": "ебать😡",
        "е***": "ебал😡",
        "Украине": "Украине🇺🇦",
        "Украина": "Украина🇺🇦",
        "Украину": "Украину🇺🇦",
        "Украиною": "Украиною🇺🇦"
    },
    "error": "Помилка(",
    "vidboy": "З відбоєм дупи!",
    "screenshot" : "що за? це ТЕСТУВАННЯ",
    "alert" : "та ти заїбав!!!!",
    "leave" : "Не витримав цього тиску та змився((",
    "end": "<a href='https://savelife.in.ua/donate/'>Слава Україні🇺🇦🇺🇦🇺🇦</a>",
    "youbot1": "Привіт",
    "youbot2": "Ти бот",
    "start": 'Хай! \n\nТак, я трохи дивний бот, але взагалі я прикольний бот:) \nЯ можу твої тики-токи та ютубчик зі звичайного посилання у видосик конвертувати... Ну тобі ж лінь скачати відео, правда?)\nПовідомляю і хуесошу, коли хуйло хоче запустити в Дніпро ракету, також радію з Вами, коли скасовують тривогу\nЄ ще декілька функцій... Але про них дізнаєтеся пізніше) \n\nУсім любові та миру, крім довбанутих(сосіян)❤️',
    "map_siren": "Карта оновлюється постійно до відбою",
    "ptn_xuilo": [
        'путін хуйло',
        'Їбав я путіна у сраку!',
        'Путін пішов нахуй!',
        'Ебал я путіна!',
        'путін хуйло!',
        'путін підорас!',
        'путін підор',
        'Нахуй путіна!',
        'Коли ж здохне путін?!',
        'путін смокче у ЗСУ',
        'Як же цей лисик заебал ...',
        'путін на аві, а мати у канаві',
        'путіна пора відправити в дурку',
        'Покажіть вже путіну Слідана, а то задовбав захищати...'
        ]
}
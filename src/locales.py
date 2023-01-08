import os
from dotenv import load_dotenv

#import .env file
load_dotenv()
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

localisation = {
    "load_v2t": "зачекай... намагаюсь зрозуміти твою солов'їну",
    "fail_v2t": "Ні чорта не зрозумів🤬",
    "local_v2t":{
        "идинахуй": "иди нахуй😡",
        "Путин": "хуйло🤬",
        "Росси": "соси😡",
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
        ],
    "img": {
        'light': 'AgACAgIAAxkBAAISAWO6vp-F6zG2VdiQZqCZ3Gx37F_JAAILxjEbefLQSbfbDTuCvs_8AQADAgADeQADLQQ',
        'dark': 'AgACAgIAAxkBAAISA2O6vqv__idHf1t8ClEwgf-u3mp7AAIMxjEbefLQSYijIoX7u60VAQADAgADeQADLQQ',
        'light_sqr': 'AgACAgIAAxkBAAIR_WO6vjrvqpup_nw04n4S_pHGfSVwAAIIxjEbefLQSdgbt0A4Kw6OAQADAgADeQADLQQ',
        'dark_sqr': 'AgACAgIAAxkBAAIR-2O6vizMq4QpO2JTA8kr9bSAnnnSAAKbwzEb-_jZSWP8wkX-M6YaAQADAgADeQADLQQ'
    },
    'error_img':{
        'light_sqr': 'AgACAgIAAxkBAAISCWO6vueB0JJvpHoZ1PDEQtMyFNGTAAIOxjEbefLQSVpUkL05R4qYAQADAgADeQADLQQ',
        'dark_sqr': 'AgACAgIAAxkBAAISCGO6vuLoR_nDqLCO-L3EnsARXvbTAAINxjEbefLQSSAKInAzsc9TAQADAgADeQADLQQ'
    }
}
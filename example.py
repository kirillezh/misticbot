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

localisation = {
    "load_v2t": "зачекай... намагаюсь зрозуміти твою солов'їну",
    "fail_v2t": "Ні чорта не зрозумів🤬",
    "local_v2t":{
        "Путин": "хуйло🤬",
        "Росси": "соси",
        "б****": "блядь",
        "с***": "сука",
        "н****": "нахуй",
        "п******": "підорас",
        "п*****": "піздец",
        "п****": "пізда",
        "Украине": "Украине🇺🇦",
        "Украина": "Украина🇺🇦",
        "Украину": "Украину🇺🇦",
        "Украиною": "Украиною🇺🇦"
    },
    "vidboy": "З відбоєм дуби!",
    "screenshot" : "що за? це ТЕСТУВАННЯ",
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
        ]
}
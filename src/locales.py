import os
from dotenv import load_dotenv

#import .env file
load_dotenv()

#API_ID = int(os.getenv('API_ID'))
#API_HASH = os.getenv('API_HASH')

CHAT_ID = int(os.getenv('CHAT_ID'))

API_TOKEN = os.getenv('API_TOKEN')

API_TOKEN_ALERT = os.getenv('API_TOKEN_ALERT')

DRIVER = os.getenv('DRIVER')

#CHANNEL = os.getenv('CHANNEL')

URL = os.getenv('URL')

GMT = int(os.getenv('GMT'))

#SIREN = os.getenv('SIREN')
#ENDSIREN = os.getenv('END')

LEVELLOGGINING = str(os.getenv('LEVELLOGGINING'))


localisation = {
    'ua': {
        "name": "Українська🇺🇦",
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
        "vidboy": "Загроза минула! Повертайтесь до своїх справ!",
        "screenshot" : "Поточна карта тривог",
        "leave" : "Не витримав цього тиску та змився((",
        "end": "<a href='https://savelife.in.ua/donate/'>Слава Україні🇺🇦🇺🇦🇺🇦</a>",
        "version": "Версія",
        "youbot1": "Привіт",
        "youbot2": "Ти бот",
        "start": 'Хай! \n\nТак, я трохи дивний бот, але взагалі я прикольний бот:) \nЯ можу твої тики-токи та ютубчик зі звичайного посилання у видосик конвертувати... Ну тобі ж лінь скачати відео, правда?)\nПовідомляю і хуесошу, коли хуйло хоче запустити в Дніпро ракету, також радію з Вами, коли скасовують тривогу\nЄ ще декілька функцій... Але про них дізнаєтеся пізніше) \n\nУсім любові та миру, крім довбанутих(сосіян)❤️',
        "map_siren": "Карта оновлюється постійно до відбою",
        "sirenMessage": "Тривога в",
        "settings": {
            "main":{
                "text": "<b>Налаштування</b>",
                "toMain": "<- Назад",
                "setLang": "Мова",
                "setAccess": "Рівень доступу",
                "set_Alert": "Сповіщення про тривогу",
                "setCity": "Місто",
                "set_Voicy": "Транскрипція войсів/кружечків",
                "set_TikTok": "Tiktok",
                "set_Youtube": "YouTube",
                "set_Reels": "Instagram(тільки Reels)",
                "set_Twitter": "Twitter",
                "exit": "Завершити",
                "final": "<b>Налаштування завершено✅</b>"
            },
            "error":{
                "personal": "Для особистого облікового запису ця функція недоступна. Додайте бота до групи для використання цієї функції.",
                "level": "У вас нема доступу до налаштувань."
            },
            "role":{
                "creator": "Власник",
                "administrator": "Адміни",
                "member": "Користувачі(усі)"
            }
        }
    },
    'en': {
        "name": "English",
        "load_v2t": "wait... trying to understand your text",
        "fail_v2t": "I didn't get it at all 🤬",
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
        "error": "Error",
        "vidboy": "Air Raid Clearance",
        "screenshot" : "Current alarm map",
        "leave" : "Couldn't stand this pressure and washed away((",
        "end": "<a href='https://savelife.in.ua/donate/'>Glory to Ukraine🇺🇦🇺🇦🇺🇦</a>",
        "version": "Version",
        "youbot1": "Hello",
        "youbot2": "You are a bot",
        "start": 'Hy! \n\nYes, I\'m a bit of a strange bot, but in general I\'m a cool bot:) \nI can convert your tiktoks and YouTube videos from a normal link to a video... Well, you\'re too lazy to download videos, aren\'t you?)\nI also inform Huesosha, when the bastard wants to launch a rocket into the Dnipro, I am also happy with you when the alarm is canceled\nThere are a few more functions... But you will learn about them later) \n\nLove and peace to all, except for the dovbanut(susians)❤️',
        "map_siren": "The map is constantly updated until it crashes",
        "sirenMessage": "Siren in",
        "settings": {
            "main":{
                "text": "<b>Settings</b>",
                "toMain": "<- Back",
                "setLang": "Language",
                "setAccess": "Access level",
                "set_Alert": "Notification about alerts",
                "setCity": "City",
                "set_Voicy": "Transcription of voices",
                "set_TikTok": "Tiktok",
                "set_Youtube": "YouTube",
                "set_Twitter": "Twitter",
                "set_Reels": "Instagram(only Reels)",
                "exit": "Finish",
                "final": "<b>Setting complete ✅</b>"
            },
            "error":{
                "personal": "This feature is not available for a personal account. Add the bot to the group to use this feature."
            },
            "role":{
                "creator": "Owner",
                "administrator": "Admins",
                "member": "Users(all)"
            }
        }
     }
}

cities = {
    "Дніпропетровська область": "Dnipropetrovsk",
    "Київська область": "Kyiv Region",
    "м. Київ": "Kyiv city",
    "Рівненська область": "Rivne",
    "Житомирська область": "Zhytomyr",
    "Закарпатська область": "Zakarpattia",
    "Хмельницька область": "Khmelnytskyi",
    "Крим": "Autonomous Republic of Crimea",
    "Черкаська область": "Cherkasy",
    "Чернігівська область": "Chernihiv",
    "Чернівецька область": "Chernivtsi",
    "Донецька область": "Donetsk",
    "Івано-Франківська область": "Ivano-Frankivsk",
    "Харківська область": "Kharkiv",
    "Херсонська область": "Kherson",
    "Кіровоградська область": "Kirovohrad",
    "Луганська область": "Luhansk",
    "Львівська область": "Lviv",
    "Миколаївська область": "Mykolaiv",
    "Одеська область": "Odesa",
    "Полтавська область": "Poltava",
    "Сумська область": "Sumy",
    "Тернопільська область": "Ternopil",
    "Вінницька область": "Vinnytsia",
    "Волинська область": "Volyn",
    "Запорізька область": "Zaporizhia"
}

defenitionAPIUID = {
    '9': "Dnipropetrovsk",
    '14': "Kyiv Region",
    '31': "Kyiv city",
    '5': "Rivne",
    '10': "Zhytomyr",
    '11': "Zakarpattia",
    '3': "Khmelnytskyi",
    '29': "Autonomous Republic of Crimea",
    '24': "Cherkasy",
    '25': "Chernihiv",
    '26': "Chernivtsi",
    '28': "Donetsk",
    '13': "Ivano-Frankivsk",
    '22': "Kharkiv",
    '23': "Kherson",
    '15': "Kirovohrad",
    '16': "Luhansk",
    '27': "Lviv",
    '17': "Mykolaiv",
    '18': "Odesa",
    '19': "Poltava",
    '20': "Sumy",
    '21': "Ternopil",
    '4': "Vinnytsia",
    '8': "Volyn",
    '12': "Zaporizhia"
}
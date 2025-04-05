import re
import random
import datetime
import locale
import webbrowser
import requests
from textblob import TextBlob
from googletrans import Translator
import spacy

locale.setlocale(locale.LC_ALL, "Russian")
API_KEY = "9303b20b05c95a33fed3ef81df34f36f"
translator = Translator()
nlp = spacy.load("ru_core_news_sm")

# Функция лемматизации
def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])

def search(match):
    query = match.group(1)
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Вот результаты поиска по запросу: {query}"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"В городе -{city}- сейчас {weather_desc} при температуре {temp}°C."
    else:
        return "Не удалось получить информацию о погоде. Попробуйте другой город."

responses = {
    r"привет": [
        "Привет! Как я могу помочь?",
        "Привет, снова появились вопросы?)",
        "Здравствуй! Рад тебя видеть!"
    ],
    r"здравствуй": [
        "Привет! Как я могу помочь?",
        "Привет, снова появились вопросы?)",
        "Здравствуй! Рад тебя видеть!"
    ],
    r"как тебя зовут\?": [
        "Я бот-помощник!",
        "Я бот-гений, нет никого гениальнее меня, задавай свой вопрос)",
        "Мое имя - Бот, Бот-помощник, и я уже жду твоего вопроса!"
    ],
    r"кто ты\?": [
        "Я бот-помощник!",
        "Я бот-гений, нет никого гениальнее меня, задавай свой вопрос)",
        "Мое имя - Бот, Бот-помощник, и я уже жду твоего вопроса!"
    ],
    r"что ты умеешь\?": [
        "Я умею отвечать на простые вопросы. Попробуй спросить: 'Как тебя зовут?', 'Сколько времени?' или попробуй ввести числа, чтобы я их суммировал, например 'сложи 5 + 5'",
        "Я знаю погоду в любом городе мира, вычисляю операции с числами, а также могу сделать за тебя запрос в интернете!",
        "Я же гений, я умею всё! (ну или почти)"
    ],
    r"сколько времени\?": lambda _: f"Сейчас {datetime.datetime.now().strftime('%H:%M:%S')}",
    r"какое сегодня число и день недели\?": lambda _: f"Сегодня {datetime.datetime.now().strftime('%d.%m.%y')}, {datetime.datetime.now().strftime('%A')}",
    r"какое сегодня число\?": lambda _: f"Сегодня {datetime.datetime.now().strftime('%d.%m.%y')}",
    r"какой сегодня день недели\?": lambda _: f"Сегодня {datetime.datetime.now().strftime('%A')}",
    r"что можешь сказать о погоде сегодня\?": "Погода говорит одно: 'выйди на улицу и погуляй'!",
    r"сложи ([\d.]+)\s*\+\s*([\d.]+)\??": lambda m: str(round(float(m.group(1)) + float(m.group(2)), 1)),
    r"вычти ([\d.]+)\s*-\s*([\d.]+)\??": lambda m: str(round(float(m.group(1)) - float(m.group(2)), 1)),
    r"перемножь ([\d.]+)\s*\*\s*([\d.]+)\??": lambda m: str(round(float(m.group(1)) * float(m.group(2)), 1)),
    r"раздели ([\d.]+)\s*/\s*([\d.]+)\??": lambda m: str(round(float(m.group(1)) / float(m.group(2)), 1))
    if float(m.group(2)) != 0 else "Бесконечность не предееееел! (на ноль не люблю делить, да и нельзя)",
    r"поиск\s+(.+)": search,
    r"погода в\s+(.+)": lambda m: get_weather(m.group(1))
}

def sentiment_response(text):
    blob = TextBlob(text)
    try:
        translated_text = translator.translate(text, dest='en').text
        polarity = TextBlob(translated_text).sentiment.polarity
    except Exception:
        polarity = blob.sentiment.polarity
    if polarity > 0:
        return random.choice([
            "Ого, ты в хорошем настроении! Это радует!",
            "Позитивчик ловлю от тебя!",
            "Ты явно на волне позитива!"
        ])
    elif polarity < 0:
        return random.choice([
            "Что-то ты грустный... Давай я попробую поднять настроение!",
            "Не грусти, всё наладится!",
            "Чувствую негатив... Может, поговорим об этом?"
        ])
    else:
        return random.choice([
            "Нейтрально как-то... расскажи больше!",
            "Ты в спокойном настроении — это тоже круто.",
            "Хмм, звучит довольно ровно. Что ещё расскажешь?"
        ])

def chatbot_response(text):
    original_text = text
    text = lemmatize_text(text.lower())
    sentiment_reply = sentiment_response(original_text)

    for pattern, response in responses.items():
        match = re.match(pattern, text)
        if match:
            if isinstance(response, list):
                return f"{sentiment_reply}\n{random.choice(response)}"
            return f"{sentiment_reply}\n{response(match) if callable(response) else response}"
    return f"{sentiment_reply}\n{random.choice(['Я не понял вопрос.', 'Попробуйте перефразировать.'])}"

if __name__ == "__main__":
    print("Введите 'выход' для завершения диалога.")

    with open("chat_log.txt", "w", encoding="utf-8") as log_file:
        pass

    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        while True:
            user_input = input("Вы: ")

            log_file.write(f"Пользователь: {user_input}\n")

            if user_input.lower() == "выход":
                exit_messages = ["До свидания!", "Буду ждать снова!", "Ещё увидимся! Пока!"]
                bot_exit_message = random.choice(exit_messages)
                print(f"Бот: {bot_exit_message}")
                log_file.write(f"Бот: {bot_exit_message}\n")
                log_file.write("-" * 40 + "\n")
                break

            bot_response = chatbot_response(user_input)
            print(f"Бот: {bot_response}")
            log_file.write(f"Бот: {bot_response}\n")
            log_file.write("-" * 40 + "\n")

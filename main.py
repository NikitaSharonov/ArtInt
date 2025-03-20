import re
import random
import datetime
import locale

locale.setlocale(locale.LC_ALL, "Russian")

# Определяем словарь шаблонов и ответов
responses = {
    r"привет": "Привет! Как я могу помочь?",
    r"здравствуй": "Привет! Как я могу помочь?",
    r"как тебя зовут\?": "Я бот-помощник!",
    r"кто ты\?": "Я бот-помощник!",
    r"что ты умеешь\?": "Я умею отвечать на простые вопросы. "
                        "Попробуй спросить: 'Как тебя зовут?', 'сколько времени?' или попробуй ввести числа, "
                        "чтобы я их суммировал, например 'сложи 5 + 5'",
    r"сколько времени\?": f"Сейчас {datetime.datetime.now().strftime("%H:%M:%S")}",
    r"какое сегодня число и день недели\?": f"Сегодня {datetime.datetime.now().strftime("%d.%m.%y")}, {datetime.datetime.now().strftime("%A")}",
    r"какое сегодня число\?": f"Сегодня {datetime.datetime.now().strftime("%d.%m.%y")}",
    r"какой сегодня день недели\?": f"Сегодня {datetime.datetime.now().strftime("%A")}",
    r"что можешь сказать о погоде сегодня\?": "Погода говорит одно: 'выйди на улицу и погуляй'!",
    r"сложи ([\d.]+)\s*\+\s*([\d.]+)\??": lambda m: str(round(float(m.group(1)) + float(m.group(2)), 1)),
    r"вычти ([\d.]+)\s*-\s*([\d.]+)\??": lambda m: str(round(float(m.group(1)) - float(m.group(2)), 1)),
    r"перемножь ([\d.]+)\s*\*\s*([\d.]+)\??": lambda m: str(round(float(m.group(1)) * float(m.group(2)), 1)),
    r"раздели ([\d.]+)\s*/ \s*([\d.]+)\??": lambda m: str(round(float(m.group(1)) / float(m.group(2)), 1))
    if float(m.group(2)) != 0 else "Бесконечность не предееееел! (на ноль не люблю делить, да и нельзя)",
}

def chatbot_response(text):
    text = text.lower()  # Приведение к нижнему регистру для унификации
    for pattern, response in responses.items():
        match = re.match(pattern, text)
        if match:
            return response(match) if callable(response) else response
    return random.choice(["Я не понял вопрос.", "Попробуйте перефразировать."])

if __name__ == "__main__":
    print("Введите 'выход' для завершения диалога.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "выход":
            print("Бот: До свидания!")
            break
        print("Бот:", chatbot_response(user_input))

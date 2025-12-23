import telebot
from telebot.types import Message
import requests

API_URL = "http://127.0.0.1:8000/api"
BOT_TOKEN = "8510736380:AAGUqoCF48JSD6kafMyY8gp1tesUnQuTJqE"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message: Message):
    data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username or ""
    }
    response = requests.post(API_URL + "/register/", json=data)

    try:
        resp_json = response.json()
    except ValueError:
        resp_json = None

    # 1) Успешная регистрация
    if response.status_code in (200, 201) and isinstance(resp_json, dict):
        bot.send_message(
            message.chat.id,
            f"Вы успешно зарегистрированы! Ваш уникальный номер: {resp_json.get('id')}"
        )
        return

    # 2) Пользователь уже есть (твой API возвращает 400 с error)
    if response.status_code == 400 and isinstance(resp_json, dict):
        err = (resp_json.get("error") or "").lower()
        if "already exists" in err or "exists" in err:
            bot.send_message(message.chat.id, "Вы уже были зарегистрированы ранее!")
            return

    # 3) Любая другая ошибка
    bot.send_message(message.chat.id, "Произошла ошибка при регистрации!")
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)
    print("JSON:", resp_json)

@bot.message_handler(commands=['myinfo'])
def user_info(message: Message):
    response = requests.get(f"{API_URL}/user/{message.from_user.id}/")

    if response.status_code == 200:
        bot.reply_to(message, f"Ваша регистрация:\n\n{response.json()}")
    elif response.status_code == 404:
        bot.send_message(message.chat.id, "Вы не зарегистрированы!")
    else:
        bot.send_message(message.chat.id, "Непредвиденная ошибка!")





if __name__ == "__main__":
    bot.polling(none_stop=True)
